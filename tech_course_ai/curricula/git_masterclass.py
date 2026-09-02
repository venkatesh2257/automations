"""
Git & GitHub Masterclass Curriculum (15 Structured Lessons)
From Fundamentals to Advanced Production Workflows
"""

GIT_COURSE = {
    "id": "git_masterclass",
    "title": "Git & GitHub Masterclass: From Zero to Senior Engineer",
    "description": "Master version control, collaboration, conflict resolution, rebase workflows, and GitHub CI/CD.",
    "category": "DevOps & Core Tools",
    "lessons": [
        {
            "lesson_number": 1,
            "title": "What is Version Control & Why Developers Can't Live Without It",
            "concept": "The problem of file tracking, history snapshots, and distributed collaboration.",
            "analogy": "A video game save checkpoint system vs saving over a single file.",
            "key_commands": ["git --version", "git config --global user.name", "git config --global user.email"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 2,
            "title": "Git Internal Architecture: Working Directory, Staging Area, & Repository",
            "concept": "The 3 states of Git files: Modified, Staged, and Committed.",
            "analogy": "A photo studio: Working dir is the set, Staging is posing for the photo, Commit is snapping the shutter.",
            "key_commands": ["git init", "git status", "git add <file>", "git commit -m 'message'"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 3,
            "title": "Inspecting History: Git Log, Git Diff, & Commit Hashes",
            "concept": "Understanding commit SHAs, author metadata, inspecting exact file changes, and reading diffs.",
            "analogy": "A blockchain audit trail showing who changed what line of code and when.",
            "key_commands": ["git log --oneline --graph", "git diff", "git diff --staged", "git show <hash>"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 4,
            "title": "Git Branching: Creating Parallel Universes for Your Code",
            "concept": "How branches work as lightweight movable pointers to commits without duplicating files.",
            "analogy": "Multiverse timelines: experimenting freely on an alternate timeline without breaking production.",
            "key_commands": ["git branch <name>", "git switch <name>", "git checkout -b <name>", "git branch -d <name>"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 5,
            "title": "Merging & Fast-Forward Merges Explained",
            "concept": "Bringing branches together, 3-way merge commits vs fast-forward merges.",
            "analogy": "Merging two highway lanes into one seamless road.",
            "key_commands": ["git merge <branch>", "git merge --no-ff <branch>"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 6,
            "title": "Mastering Merge Conflicts Like a Senior Engineer",
            "concept": "Why conflicts happen when two branches touch the exact same lines, and how to resolve them cleanly.",
            "analogy": "Two editors editing the same paragraph with different text—you must pick the best version.",
            "key_commands": ["git merge", "git status", "git add <resolved-file>", "git commit"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 7,
            "title": "Connecting to GitHub & Remote Repositories",
            "concept": "Origin, upstream, SSH keys vs Personal Access Tokens, pushing, pulling, and tracking branches.",
            "analogy": "Syncing your local Google Drive folder to the cloud server.",
            "key_commands": ["git remote add origin <url>", "git push -u origin main", "git fetch", "git pull"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 8,
            "title": "Git Rebase vs Git Merge: The Ultimate Showdown",
            "concept": "Linear commit history vs true historical timeline, rewiring the base commit.",
            "analogy": "Re-stacking bricks in a neat single tower instead of a tangled web.",
            "key_commands": ["git rebase main", "git rebase -i HEAD~3", "git rebase --continue", "git rebase --abort"],
            "difficulty": "Advanced"
        },
        {
            "lesson_number": 9,
            "title": "The Power of Git Stash: Saving Unfinished Work Instantly",
            "concept": "Temporarily shelving dirty working directory changes without creating a half-baked commit.",
            "analogy": "Putting your current puzzle on a shelf while you deal with an urgent emergency, then picking it back up.",
            "key_commands": ["git stash", "git stash pop", "git stash list", "git stash apply"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 10,
            "title": "Undoing Mistakes: Git Reset vs Git Revert vs Git Restore",
            "concept": "Soft vs Mixed vs Hard reset, safe undoing with public commits vs rewriting private history.",
            "analogy": "Tearing out a page from a private notebook (Reset) vs writing an official retraction statement (Revert).",
            "key_commands": ["git restore <file>", "git reset --soft HEAD~1", "git reset --hard HEAD~1", "git revert <hash>"],
            "difficulty": "Advanced"
        },
        {
            "lesson_number": 11,
            "title": "Git Cherry-Pick: Stealing Specific Commits Across Branches",
            "concept": "Extracting a single bugfix or feature commit from another branch without merging everything.",
            "analogy": "Picking one ripe strawberry from a basket without taking the whole basket.",
            "key_commands": ["git cherry-pick <commit-hash>", "git cherry-pick -n <hash>"],
            "difficulty": "Advanced"
        },
        {
            "lesson_number": 12,
            "title": "Ignoring Files Like a Pro: Mastering .gitignore",
            "concept": "Preventing node_modules, .env secrets, and build artifacts from ever polluting version control.",
            "analogy": "A bouncer checking the VIP list at the door of your repository.",
            "key_commands": ["touch .gitignore", "git rm --cached <file>"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 13,
            "title": "GitHub Pull Requests, Code Reviews, & Branch Protection Rules",
            "concept": "Collaborative workflows, PR approvals, automated status checks, and protecting the main branch.",
            "analogy": "Submitting a blueprint for peer review before construction workers pour concrete.",
            "key_commands": ["git push origin feature-branch"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 14,
            "title": "Git Bisect: Finding Bugs with Binary Search Superpowers",
            "concept": "Automating bug detection across hundreds of commits in seconds using binary search.",
            "analogy": "A detective dividing a suspect lineup in half repeatedly to find the culprit in seconds.",
            "key_commands": ["git bisect start", "git bisect bad", "git bisect good <hash>", "git bisect reset"],
            "difficulty": "Expert"
        },
        {
            "lesson_number": 15,
            "title": "Git Hooks & Automated Quality Guards",
            "concept": "Pre-commit and pre-push automated scripts running linters, tests, and secret scanners.",
            "analogy": "An automatic security scanner at the airport gate checking your luggage before boarding.",
            "key_commands": [".git/hooks/pre-commit", "npx husky init"],
            "difficulty": "Expert"
        }
    ]
}
