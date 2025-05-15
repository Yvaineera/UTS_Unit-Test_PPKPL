from data.group_repository import GroupRepository
from usecases.group_service import GroupService

def run_cli(service: GroupService):
    while True:
        print("\n=== KPOP GROUP MANAGER ===")
        print("1. Add Group")
        print("2. Browse All")
        print("3. Read Group by Name")
        print("4. Edit Group")
        print("5. Delete Group")
        print("6. Exit")

        choice = input("Choose (1-6): ")

        if choice == "1":
            name = input("Enter group name: ")
            members = int(input("Enter number of members: "))
            if service.add(name, members):
                print("✅ Group added.")
            else:
                print("⚠️ Group already exists.")

        elif choice == "2":
            groups = service.browse()
            if not groups:
                print("⚠️ No groups found.")
            for group in groups:
                print(f"- {group.name} ({group.members} members)")

        elif choice == "3":
            name = input("Enter group name to read: ")
            group = service.read(name)
            if group:
                print(f"🎤 {group.name} has {group.members} members.")
            else:
                print("❌ Group not found.")

        elif choice == "4":
            old_name = input("Enter group name to edit: ")
            new_name = input("Enter new name (leave blank to keep same): ")
            new_members = input("Enter new members (leave blank to keep same): ")
            new_members = int(new_members) if new_members.strip() else None
            result = service.edit(old_name, new_name or None, new_members)
            print("✅ Updated." if result else "❌ Edit failed.")

        elif choice == "5":
            name = input("Enter group name to delete: ")
            result = service.delete(name)
            print("✅ Deleted." if result else "❌ Group not found.")

        elif choice == "6":
            print("👋 Exiting...")
            break
        else:
            print("⚠️ Invalid option.")

if __name__ == "__main__":
    repo = GroupRepository()
    service = GroupService(repo)
    run_cli(service)