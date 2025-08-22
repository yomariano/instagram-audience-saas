const Apify = require('apify');

Apify.main(async () => {
    const input = await Apify.getInput();
    const { username, maxPosts = 10, includeComments = true, maxCommentsPerPost = 50 } = input;

    console.log(`Starting scraping for Instagram account: ${username}`);

    const browser = await Apify.launchPuppeteer({
        headless: true,
        useChrome: true,
    });

    const page = await browser.newPage();
    
    try {
        // Navigate to Instagram profile
        await page.goto(`https://www.instagram.com/${username}/`, { waitUntil: 'networkidle0' });
        
        // Wait for posts to load
        await page.waitForSelector('article', { timeout: 10000 });
        
        // Get profile info
        const profileInfo = await page.evaluate(() => {
            const followersElement = document.querySelector('a[href*="/followers/"] span');
            const followingElement = document.querySelector('a[href*="/following/"] span');
            const postsElement = document.querySelector('div span');
            
            return {
                followers: followersElement ? followersElement.textContent : '0',
                following: followingElement ? followingElement.textContent : '0',
                posts: postsElement ? postsElement.textContent : '0'
            };
        });

        console.log('Profile info:', profileInfo);

        // Get post links
        const postLinks = await page.evaluate((maxPosts) => {
            const links = Array.from(document.querySelectorAll('a[href*="/p/"]')).slice(0, maxPosts);
            return links.map(link => link.href);
        }, maxPosts);

        console.log(`Found ${postLinks.length} posts to scrape`);

        const scrapedPosts = [];

        // Scrape each post
        for (const postLink of postLinks) {
            try {
                await page.goto(postLink, { waitUntil: 'networkidle0' });
                
                // Get post data
                const postData = await page.evaluate((includeComments, maxCommentsPerPost) => {
                    const post = {
                        url: window.location.href,
                        caption: '',
                        likes: 0,
                        comments: []
                    };

                    // Get caption
                    const captionElement = document.querySelector('article div div div div span');
                    if (captionElement) {
                        post.caption = captionElement.textContent;
                    }

                    // Get likes
                    const likesElement = document.querySelector('button span');
                    if (likesElement && likesElement.textContent.includes('like')) {
                        const likesText = likesElement.textContent;
                        post.likes = parseInt(likesText.replace(/[^0-9]/g, '')) || 0;
                    }

                    // Get comments if requested
                    if (includeComments) {
                        const commentElements = Array.from(document.querySelectorAll('div[role="button"] div div div')).slice(0, maxCommentsPerPost);
                        
                        commentElements.forEach(commentEl => {
                            const usernameEl = commentEl.querySelector('span span');
                            const textEl = commentEl.querySelector('span:last-child');
                            
                            if (usernameEl && textEl) {
                                // Try to get profile picture
                                const profilePicEl = commentEl.closest('div').querySelector('img');
                                
                                post.comments.push({
                                    username: usernameEl.textContent,
                                    text: textEl.textContent,
                                    profilePic: profilePicEl ? profilePicEl.src : null
                                });
                            }
                        });
                    }

                    return post;
                }, includeComments, maxCommentsPerPost);

                scrapedPosts.push(postData);
                console.log(`Scraped post: ${postData.url} with ${postData.comments.length} comments`);

                // Small delay to avoid rate limiting
                await page.waitForTimeout(2000);

            } catch (postError) {
                console.error(`Error scraping post ${postLink}:`, postError.message);
            }
        }

        // Save results
        await Apify.pushData({
            username,
            profileInfo,
            posts: scrapedPosts,
            scrapedAt: new Date().toISOString()
        });

        console.log(`Scraping completed. Total posts: ${scrapedPosts.length}`);

    } catch (error) {
        console.error('Scraping failed:', error);
        throw error;
    } finally {
        await browser.close();
    }
});