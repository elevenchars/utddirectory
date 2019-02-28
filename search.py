import requests  # HTTP request sending library
from bs4 import BeautifulSoup  # HTML parsing library
import fire  # CLI interface


def print_email(email):
    """Print information about an email scraped from the UTD directory.

    Arguments:
        email {string} -- email to search for in the directory.
    """

    results = find_by_email(email)
    print("Name: {}".format(results["name"]))
    print("Classification: {}".format(results["classification"]))
    print("Major: {}".format(results["major"]))
    print("School: {}".format(results["school"]))


def find_by_email(email):
    """Generate a dictionary of information about an email scraped from the
       UTD directory.

    Arguments:
        email {string} -- email to search for in the directory.

    Returns:
        dict -- dictionary of information containing name, classification,
                major, and school.
    """

    # request that is called on the UTD Directory page
    endpoint_url = "https://www.utdallas.edu/directory/includes/directories.class.php"
    fields = {"dirType": "email", "dirSearch": email}  # required parameters

    resp = requests.get(endpoint_url, params=fields)  # send GET request

    soup = BeautifulSoup(resp.text, "html.parser")
    name = soup.find("h5", {"class": "fullname firstEntry"}).text
    classification, major = soup.find("span", {"class": "keepHeight"}).next_sibling.split(",")
    major = major.strip()
    # this looks kind of gross and i'm sure there is a better way to do this.
    school = soup.find("span", {"class": "keepHeight"}).next_sibling.next_sibling.next_sibling

    return {
        "name": name,
        "classification": classification,
        "major": major,
        "school": school
    }

if __name__ == "__main__":
    fire.Fire({
        "email": print_email
    })
