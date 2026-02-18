pipeline {
  agent any
  options {
    timestamps()
    disableConcurrentBuilds()
  }
  environment {
    DOCKER_IMAGE = 'ecommerce-api'
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        sh 'docker build -t ${DOCKER_IMAGE}:latest .'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run --rm ${DOCKER_IMAGE}:latest sh -c "pytest -q"'
      }
    }
    stage('Smoke Test') {
      steps {
        sh 'docker run --rm ${DOCKER_IMAGE}:latest sh -c "python manage.py check"'
      }
    }
    stage('Deploy to EC2') {
      steps {
        withCredentials([
          string(credentialsId: 'ec2_host', variable: 'EC2_HOST'),
          string(credentialsId: 'django_allowed_hosts', variable: 'ALLOWED_HOSTS'),
          string(credentialsId: 'django_debug', variable: 'DJANGO_DEBUG'),
        ]) {
          sshagent(credentials: ['ec2_ssh']) {
            sh '''
              ssh -o StrictHostKeyChecking=no ${EC2_HOST} "cd ~/ecommerce-api && git pull && export DJANGO_ALLOWED_HOSTS='${ALLOWED_HOSTS}' && export DJANGO_DEBUG='${DJANGO_DEBUG}' && bash scripts/deploy_ec2.sh"
            '''
          }
        }
      }
    }
  }
  post {
    always {
      sh 'docker image ls ${DOCKER_IMAGE} | head -n 5'
    }
  }
}
