import requests  # HTTP request sending library
from bs4 import BeautifulSoup  # HTML parsing library
import fire  # CLI interface


def print_email(email: str) -> None:
    """Print information about an email scraped from the UTD directory.

    Arguments:
        email {str} -- email to search for in the directory

    Returns:
        None -- no return type, prints to the console.
    """

    results = find_by_email(email)
    if results:  # if not None:
        print("Name: {}".format(results["name"]))
        print("Classification: {}".format(results["classification"]))
        print("Major: {}".format(results["major"]))
        print("School: {}".format(results["school"]))
    else:
        print("No information found.")


def find_by_email(email: str) -> dict:
    """Generate a dictionary of information about an email scraped from the
       UTD directory.

    Arguments:
        email {str} -- email to search for in the directory

    Returns:
        dict -- dictionary of information containing name, classification,
                major, and school.
    """

    # request that is called on the UTD Directory page
    endpoint_url = "https://www.utdallas.edu/directory/includes/directories.class.php"
    fields = {"dirType": "email", "dirSearch": email}  # required parameters

    resp = requests.get(endpoint_url, params=fields)  # send GET request

    # create HTML parser for the response
    soup = BeautifulSoup(resp.text, "html.parser")

    # if there is no user found (<p class='dirAlert'> present)
    if soup.find("p", {"class": "dirAlert"}):
        return None

    # find name in the response
    name = soup.find("h5", {"class": "fullname firstEntry"}).text

    # since classification and major are in the same line we need to split
    classification, major = soup.find("span", {"class": "keepHeight"}).next_sibling.split(",")
    major = major.strip()  # get rid of extra whitespace
    # this looks kind of gross and i'm sure there is a better way to do this
    school = soup.find("span", {"class": "keepHeight"}).next_sibling.next_sibling.next_sibling

    return {
        "name": name,
        "classification": classification,
        "major": major,
        "school": school
    }

if __name__ == "__main__":
    # create command line interface, and only expose the print_email method.
    fire.Fire({
        "email": print_email
    })
