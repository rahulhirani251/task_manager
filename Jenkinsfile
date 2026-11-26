pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    // GitHub webhook na ho (local Jenkins) to har 2 minute mein repo check karega
    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        APP_ENV = 'testing'
        VENV    = '.venv'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Dependencies install ho rahi hain...'
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m py_compile app.py
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Tests chal rahe hain...'
                sh '''
                    . ${VENV}/bin/activate
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Deploy') {
            // Sirf main branch se deploy hoga
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                }
            }
            steps {
                echo 'Deploy ho raha hai...'
                // Jenkins > Credentials mein "Secret text" banao, ID: render-deploy-hook
                withCredentials([string(credentialsId: 'render-deploy-hook', variable: 'DEPLOY_HOOK')]) {
                    sh 'curl -fsS -X POST "$DEPLOY_HOOK"'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful: Build, Test aur Deploy complete.'
        }
        failure {
            echo 'Pipeline fail ho gayi, console output check karo.'
        }
        cleanup {
            cleanWs()
        }
    }
}
