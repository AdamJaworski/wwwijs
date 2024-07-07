from managers.database import *

if __name__ == "__main__":
    for i in range(1, 5):
        add_organization(f'test_org{i}')
        assign_user_to_organization('test', f'test_org{i}', 5)

    for org in range(1, 5):
        for i in range(1, 5):
            add_task(i, f"task {i}", f"test_org{org}", 5, f'task {i} title')