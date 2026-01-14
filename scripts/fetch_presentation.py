#!/usr/bin/env python3
"""
Fetch presentation content from Canva using Playwright
"""
import asyncio
import sys
from playwright.async_api import async_playwright


async def fetch_presentation(url):
    """Fetch and extract text content from a Canva presentation."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()

        print('Loading presentation...', file=sys.stderr)

        try:
            await page.goto(url, wait_until='networkidle', timeout=45000)

            # Wait for Canva to render
            await page.wait_for_timeout(5000)

            # Get the page title
            title = await page.title()
            print(f'Page Title: {title}', file=sys.stderr)

            all_slides_content = []
            all_slides_content.append(f"# {title}\n")

            # Try to find total number of slides
            page_indicator = await page.query_selector('[aria-label*="page"]')
            if not page_indicator:
                page_indicator = await page.query_selector('text=/\\d+\\s*\\/\\s*\\d+/')

            # Navigate through slides using keyboard
            max_slides = 15  # Safety limit
            seen_content = set()

            for slide_num in range(max_slides):
                await page.wait_for_timeout(1000)

                # Extract current slide content
                content = await page.inner_text('body')

                # Clean up the content - remove UI elements
                lines = content.split('\n')
                clean_lines = []
                skip_patterns = ['Canva', 'Share', 'opens in a new tab', 'Zoom',
                                'Enter full screen', 'Toolbar', 'Slide controls',
                                'Previous page', 'Next page', 'Go to page', 'More',
                                'AAAA', 'Slide content']

                for line in lines:
                    line = line.strip()
                    if not line or len(line) < 3:
                        continue
                    if any(skip in line for skip in skip_patterns):
                        continue
                    if line not in seen_content:
                        seen_content.add(line)
                        clean_lines.append(line)

                if clean_lines:
                    all_slides_content.append(f"\n## Slide {slide_num + 1}\n")
                    all_slides_content.extend(clean_lines)

                # Press right arrow to go to next slide
                await page.keyboard.press('ArrowRight')
                await page.wait_for_timeout(500)

                # Check if we've reached the end (content stops changing)
                new_content = await page.inner_text('body')
                if slide_num > 0 and new_content == content:
                    print(f'Reached end at slide {slide_num + 1}', file=sys.stderr)
                    break

            await browser.close()
            return '\n'.join(all_slides_content)

        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)
            await browser.close()
            return None


async def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_presentation.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = await fetch_presentation(url)

    if content:
        print("=" * 60)
        print("PRESENTATION CONTENT")
        print("=" * 60)
        print(content)
    else:
        print("Failed to fetch presentation content")


if __name__ == '__main__':
    asyncio.run(main())
