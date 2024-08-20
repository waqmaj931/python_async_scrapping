import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_and_scrape(session, url):
    async with session.get(url) as response:
        content = await response.text()
        print(f"Fetched {url} with response length {len(content)}")
        
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the title of the webpage
        title = soup.title.string if soup.title else 'No Title'
        
        # Extract all paragraph text
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        
        return url, title, paragraphs

async def scrape_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_scrape(session, url) for url in urls]
        return await asyncio.gather(*tasks)

def save_to_file(scraped_data, filename="scraped_data.txt"):
    with open(filename, 'w') as file:
        for url, title, paragraphs in scraped_data:
            file.write(f"URL: {url}\n")
            file.write(f"Title: {title}\n")
            file.write("Paragraphs:\n")
            for paragraph in paragraphs:
                file.write(f"  - {paragraph}\n")
            file.write("\n\n")

if __name__ == "__main__":
    urls = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    
    scraped_data = asyncio.run(scrape_all(urls))
    save_to_file(scraped_data)

    print(f"Scraped data from {len(scraped_data)} URLs and saved to 'scraped_data.txt'")
