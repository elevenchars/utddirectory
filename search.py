import requests  # HTTP request sending library
from bs4 import BeautifulSoup  # HTML parsing library
import fire  # CLI interface
from enum import Enum


class SearchType(Enum):
    NAME = "displayname"
    EMAIL = "email"
    PHONE_NUMBER = "telephonenumber"


def print_info(search_type: SearchType, query: str) -> None:
    """Print information about a person, scraped from the UTD directory

    Arguments:
        type {SearchType} -- Type of search being done
        query {str} -- String to search (see SearchType class)

    Returns:
        None -- Nothing, output is printed
    """

    results = search(search_type, query)
    if results:  # if not None:
        print("Name: {}".format(results["name"]))
        print("Email: {}".format(results["email"]))
        print("Classification: {}".format(results["classification"]))
        print("Major: {}".format(results["major"]))
        print("School: {}".format(results["school"]))
    else:
        print("No information found.")


def search(search_type: SearchType, query: str) -> dict:
    """Find information about a person, scraped from the UTD directory.

    Arguments:
        type {SearchType} -- Type of query to run: see values of SearchType
        query {str} -- String to be searched. (see SearchType class)

    Returns:
        dict -- Dictionary with name, email, classification, major, school
        None -- user was not found using search parameter
    """

    # request that is called on the UTD Directory page
    endpoint_url = "https://www.utdallas.edu/directory/includes/directories.class.php"
    # required parameters to communicate with the directory server.
    fields = {"dirType": search_type.value, "dirSearch": query}

    # send GET request to the directory
    directory_request = requests.get(endpoint_url, params=fields)

    # create HTML parser for the response
    soup = BeautifulSoup(directory_request.text, "html.parser")

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

    # this is the 'security through obscurity' that the school uses
    # to hide emails.
    # the f parameter is in the webpage. it also requires cookies from
    # the first request.
    email_id = soup.find("a", {"onclick": "showEmailAddress(this.id); return false;"})["id"]
    email_params = {"f": email_id}
    email_url = "https://www.utdallas.edu/directory/includes/response.php"
    email_request = requests.get(email_url, params=email_params, cookies=directory_request.cookies)
    email_soup = BeautifulSoup(email_request.text, "html.parser")
    email = email_soup.find("a").text

    return {
        "name": name,
        "email": email,  # for now, will find soon
        "classification": classification,
        "major": major,
        "school": school
    }


def search_email(email: str) -> None:
    """Search by email and print

    Arguments:
        email {str} -- email to search

    Returns:
        None -- prints to console
    """

    print_info(SearchType.EMAIL, email)


def search_name(name: str) -> None:
    """Search by name and print

    Arguments:
        name {str} -- name to search

    Returns:
        None -- prints to console
    """

    print_info(SearchType.NAME, name)


def search_number(number: str) -> None:
    """Search by phone number and print

    Arguments:
        number {str} -- phone number to search

    Returns:
        None -- prints to console
    """

    print_info(SearchType.PHONE_NUMBER, number)

if __name__ == "__main__":
    # create command line interface, and only expose the print_email method.
    fire.Fire({
        "email": search_email,
        "name": search_name,
        "number": search_number
    })
