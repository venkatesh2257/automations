"""
DevOps, Docker & Cloud Engineering Curriculum (20 Structured Lessons)
"""

DEVOPS_COURSE = {
    "id": "devops_cloud",
    "title": "DevOps & Cloud Engineering: Zero to Production Hero",
    "description": "Master Linux, Docker containers, CI/CD pipelines, Kubernetes orchestration, and Cloud architecture.",
    "category": "DevOps & Cloud",
    "lessons": [
        {
            "lesson_number": 1,
            "title": "What is DevOps? The Philosophy, Culture & Toolchain",
            "concept": "Bridging Software Development and IT Operations to deliver code reliably and fast.",
            "analogy": "A Formula 1 pit crew working seamlessly with the driver to win the race.",
            "key_commands": ["uname -a", "df -h", "top"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 2,
            "title": "Linux Mastery for DevOps Engineers: Essential CLI Commands",
            "concept": "Navigating filesystems, process management, permissions (chmod/chown), and pipes.",
            "analogy": "Learning the engine controls of an aircraft.",
            "key_commands": ["ps aux | grep node", "kill -9 <pid>", "chmod 755 script.sh", "curl -I https://api.com"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 3,
            "title": "Why Docker? Virtual Machines vs Containers Explained",
            "concept": "Operating System-level virtualization, namespaces, cgroups, solving 'it works on my machine'.",
            "analogy": "Standardized shipping containers that fit onto any truck, ship, or train in the world.",
            "key_commands": ["docker --version", "docker run hello-world"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 4,
            "title": "Writing Your First Dockerfile: Anatomy of an Image",
            "concept": "FROM, WORKDIR, COPY, RUN, EXPOSE, and CMD instructions. Layer caching mechanics.",
            "analogy": "A cooking recipe that produces the exact same delicious meal every single time.",
            "key_commands": ["docker build -t myapp:1.0 .", "docker images"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 5,
            "title": "Docker Multi-Stage Builds: Shrinking Images from 1GB to 20MB",
            "concept": "Separating compilation environment from runtime production image for security and speed.",
            "analogy": "Building a car in a giant factory, but only shipping the finished car to the customer.",
            "key_commands": ["docker build -t myapp:slim .", "docker history myapp:slim"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 6,
            "title": "Docker Compose: Orchestrating Multi-Container Applications",
            "concept": "Managing Frontend, Backend, Database, and Redis in a single declarative YAML file.",
            "analogy": "A conductor directing an orchestra of musicians playing together in harmony.",
            "key_commands": ["docker compose up -d", "docker compose ps", "docker compose down -v"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 7,
            "title": "CI/CD Explained: Continuous Integration vs Continuous Deployment",
            "concept": "Automating test execution, building artifacts, and deploying to staging/production on git push.",
            "analogy": "An automated robotic assembly line inspecting and painting cars before they ship.",
            "key_commands": ["git push origin main"],
            "difficulty": "Beginner"
        },
        {
            "lesson_number": 8,
            "title": "GitHub Actions Masterclass: Writing Your First Automated Pipeline",
            "concept": "Workflows, Triggers, Jobs, Steps, Runners, and GitHub Secrets management.",
            "analogy": "A checklist that automatically executes every time a developer opens a pull request.",
            "key_commands": [".github/workflows/ci.yml"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 9,
            "title": "Why Kubernetes? Solving Container Sprawl at Scale",
            "concept": "Self-healing, auto-scaling, load balancing, zero-downtime rolling updates.",
            "analogy": "An air traffic control tower managing hundreds of airplanes simultaneously.",
            "key_commands": ["kubectl version --client"],
            "difficulty": "Intermediate"
        },
        {
            "lesson_number": 10,
            "title": "Kubernetes Architecture: Control Plane, Nodes, Pods, and Services",
            "concept": "API Server, etcd, Scheduler, Kubelet, Pod lifecycle, ClusterIP vs NodePort vs LoadBalancer.",
            "analogy": "A modern hospital: The director's office (Control Plane) organizing doctors and beds (Nodes/Pods).",
            "key_commands": ["kubectl get pods -A", "kubectl get nodes", "kubectl describe pod <name>"],
            "difficulty": "Advanced"
        }
    ]
}
