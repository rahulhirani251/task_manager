# Task Manager API (Flask + Jenkins CI/CD)

Chhoti Python web application jisme Jenkins pipeline (Build -> Test -> Deploy) laga hua hai.

## Routes

| Method | Route | Kaam |
|--------|-------|------|
| GET | `/` | Web page (frontend) |
| GET | `/api/info` | Welcome message aur environment (JSON) |
| GET | `/health` | Health check |
| GET | `/api/tasks` | Saare tasks |
| POST | `/api/tasks` | Naya task (`{"title": "..."}`) |
| PUT | `/api/tasks/<id>` | Task done/undone toggle |
| DELETE | `/api/tasks/<id>` | Task delete |

## Local par chalana

```bash
pip install -r requirements.txt
python app.py          # http://localhost:5000
pytest -v              # tests
```

## Jenkins pipeline (`Jenkinsfile`)

1. **Build**: virtualenv + dependencies install + syntax check
2. **Test**: `pytest`, results Jenkins mein JUnit report ke tor par dikhte hain
3. **Deploy**: sirf `main` branch par, Render deploy hook call hota hai

### Jenkins local chalana (Docker)

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk17
docker logs jenkins        # initial admin password yahan milega
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y python3 python3-venv python3-pip curl"
```

Phir http://localhost:8080 kholo, suggested plugins install karo.

### Job banana
1. New Item -> **Pipeline** (ya Multibranch Pipeline) -> naam do
2. Pipeline -> Definition: **Pipeline script from SCM** -> Git -> GitHub repo URL, branch `*/main`, Script Path: `Jenkinsfile`
3. (Deploy ke liye) Manage Jenkins -> Credentials -> **Secret text**, ID: `render-deploy-hook`, value: Render ka Deploy Hook URL
4. **Build Now** dabao

## Environments
`APP_ENV` variable se environment set hota hai: `testing`, `staging`, `production`.