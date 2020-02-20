from github import Github
import os
import json
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

g = Github(os.environ.get("GIT_TOKEN"))

organization_name = "fuchicorp"
root_access_teams = ["devops", "bastion_root"]
non_root_access_teams = ["dev"]

fuchi_org = g.get_organization(organization_name)


bastion_access = {
    "root_access" : [],
    "non_root_access" : []
}

uniq_users = set()

def templetize_user_data(team_list:list, team_object:object):
    user_list = []

    ## Checking for user list
    if team_object.name.lower() in team_list:

        ## Iterating list of user
        logging.info(f"####### Getting all members from team <{team_object.name}>")
        for user in fuchi_org.get_team(team_object.id).get_members():

            ## Checking is the user already adeed
            if user.login not in uniq_users:

                ## Added user to uniq list
                uniq_users.add(user.login)

                ## templetizing the user data
                user_data = {"username" : user.login, "ssh-keys" : [],
                "comment" : f"<{user.name}>, <{user.email}>, <{user.company}>"}

                ## if the user has ssh keys
                if user.get_keys().totalCount:

                    ## Checking file exists if yes then delete
                    if os.path.isfile(f'{user_data["username"]}.key'):
                        os.remove(f'{user_data["username"]}.key')

                    ## Iterating list of users keys
                    for key in user.get_keys():

                        ## Adding list of keys to user data
                        user_data['ssh-keys'].append(key.key)


                        ## Createing the keys for the users
                        with open(f'{user_data["username"]}.key', 'a') as f:
                            f.write("%s\n" % key.key)


                    ## Adding usert to total list
                    user_list.append(user_data)
                else:
                    logging.warning(f"User <{user.login}> does not have ssh key uploaded on github.")

    ## Returing list of users to
    return user_list

# if not os.geteuid() == 0:
#     sys.exit("\nOnly root can run this script\n")

for team in fuchi_org.get_teams():

    # Getting root members
    root_members = templetize_user_data(root_access_teams, team)
    if root_members:
        for user in root_members:
            # print(f"""###### {user["username"]} '{user["comment"]}' {user["username"]}.key --admin""")
            # os.system(f"""sudo sh user_add.sh {user["username"]} '{user["comment"]}' {user["username"]}.key""")
            bastion_access["root_access"].append(user)

    ## Getting non root members
    non_root_members = templetize_user_data(non_root_access_teams, team)
    if non_root_members:
        for user in non_root_members:
            # print(f"""###### {user["username"]} '{user["comment"]}' {user["username"]}.key """)
            # os.system(f"""
            # sudo sh user_add.sh {user["username"]} '{user["comment"]}' {user["username"]}.key """)
            bastion_access["non_root_access"].append(user)


with open("output.json", "w") as file:
    json.dump(bastion_access, file, indent=2)