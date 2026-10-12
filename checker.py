import urllib.request
import urllib.error
import json


def get_json(url):
    try:
        response = urllib.request.urlopen(url)
        return json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


dependencies_checked = 0
packages_not_on_pypi = 0
versions_not_on_pypi = 0

oldest_year = None
oldest_name = None
oldest_version = None


with open("requirements.txt", "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        if "==" not in line:
            continue

        name, version = line.split("==", 1)

        dependencies_checked += 1

        # Check whether the package exists
        package_url = f"https://pypi.org/pypi/{name}/json"
        package_data = get_json(package_url)

        if package_data is None:
            packages_not_on_pypi += 1
            continue

        # Check whether the specific version exists
        version_url = f"https://pypi.org/pypi/{name}/{version}/json"
        version_data = get_json(version_url)

        if version_data is None:
            versions_not_on_pypi += 1
            continue

        # Package and version both exist.
        # Get the upload time of the first file.
        upload_time = version_data["urls"][0]["upload_time"]
        year = int(upload_time[:4])

        # Keep track of the oldest valid release.
        if oldest_year is None or year < oldest_year:
            oldest_year = year
            oldest_name = name
            oldest_version = version


print(f"Dependencies checked: {dependencies_checked}")
print(f"Packages not on PyPI: {packages_not_on_pypi}")
print(f"Versions not on PyPI: {versions_not_on_pypi}")
print(
    f"Oldest pinned release: "
    f"{oldest_name}=={oldest_version} ({oldest_year})"
)