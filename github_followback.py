import requests
import getpass

API = "https://api.github.com"
USERNAME = input("GitHub username: ").strip()
TOKEN = getpass.getpass("GitHub token: ").strip()

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2026-03-10"
}


def get_all(endpoint):
    users = []
    page = 1

    while True:
        response = requests.get(
            f"{API}/{endpoint}",
            headers=headers,
            params={
                "per_page": 100,
                "page": page
            }
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            break

        users.extend(user["login"] for user in data)
        page += 1

    return set(users)


print("\nFetching followers...")
followers = get_all("user/followers")

print("Fetching following...")
following = get_all("user/following")

not_following_back = sorted(following - followers)

print("\n================================")
print(f"You follow: {len(following)}")
print(f"Your followers: {len(followers)}")
print(f"Not following you back: {len(not_following_back)}")
print("================================\n")

if not not_following_back:
    print("🎉 Everyone follows you back!")
    exit()

print("People who DON'T follow you back:\n")

for user in not_following_back:
    print(f"   {user}")

print("\n================================")

confirm = input(
    f"\nUnfollow these {len(not_following_back)} people? (yes/no): "
).lower()

if confirm != "yes":
    print("\nCancelled. Nobody was unfollowed.")
    exit()

print("\nStarting unfollow...\n")

for user in not_following_back:

    response = requests.delete(
        f"{API}/user/following/{user}",
        headers=headers
    )

    if response.status_code == 204:
        print(f" Unfollowed {user}")
    else:
        print(f" Failed to unfollow {user} "
              f"(HTTP {response.status_code})")

print("\nDone ")
