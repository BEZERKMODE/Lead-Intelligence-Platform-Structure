from backend.celery_worker import celery

from backend.services.company_contact_scraper import CompanyContactScraper

scraper = CompanyContactScraper()

@celery.task
def scrape_company_contacts(url):

    return scraper.scrape_company_contacts(url)
