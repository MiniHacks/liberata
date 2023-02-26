# Liberata

_Easily find books mentioned online in libraries near you_

[Video demo (youtube)](https://youtu.be/oXjYhPLjfD4)

## Inspiration

Despite being key centers for education and community engagement, public libraries are an often underutilized civic resource that are often out of people’s minds. We believe that libraries are an important center for civil participation where people can share information, space, and other resources (for free!). 
 We built a Chrome extension to remind users that their local libraries hold media that they encounter on a daily basis..


## What it does

This extension is designed to encourage users to engage with their local libraries by highlighting books found in the text they come across on the web. With Liberata, all you have to do is scroll through your webpage. Our Chrome extension highlights books that are available in nearby libraries.  By clicking the Rat icon in the top corner, a window opens. After typing in your zip code, Rat will quickly scour your local libraries using WorldCat – a comprehensive catalog of thousands of libraries all over the globe – and report back about the locations of your books if they’re available.


## How we built it

### Frontend
The UI is a Chrome extension built using vanilla HTML, CSS, and JavaScript. Our extension was truly hacked together to serve as the delivery mechanism of the webpage content to the backend to be processed, and interpret results to display them in a friendly manner

### Backend

Our backend is written in Python and is powered by FastAPI, OpenAI GPT-3, and Playwright.. The backend does four things
- Use GPT-3 to identify book titles that are in the user's current tab
- Look up these books on WorldCat
- Find nearby libraries that have the book
- Send these library locations back to the user, along with links to place a hold on the book so that the user can check it out later

## Challenges we ran into

This was our first time building a Chrome extension -- we found it challenging to transfer our existing frontend dev knowledge to the unique environment inside Chrome.

Additionally, our project hinges on data provided by WorldCat - a nearly-comprehensive catalog of libraries worldwide. Unfortunately, they only provide API keys to organizations that run libraries. As individuals, we were left with using Playwright (a library for programmatic browser control) to scrape data off WorldCat

## Accomplishments that we're proud of

We were proud of successfully wrangling GPT-3 into providing something useful for us, even though it is notorious for hallucinating facts and ignoring instructions from time to time.

We were also proud that we were able to successfully scrape data off of WorldCat, even if our mechanism to do so was quite slow.

## What we learned

We learned how to use vanilla JS for frontend development. Talk about a throwback to the early 2000's!

