pipeline {
    agent any

    environment {
        AWS_REGION        = 'ap-south-1'
        AWS_ACCOUNT_ID    = '971089639220'        // REPLACE THIS
        ECR_REPO          = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/flask-ecs-cicd-lab"
        ECS_CLUSTER       = 'flask-ecs-cluster'
        ECS_SERVICE       = 'flask-app-service'
        IMAGE_TAG         = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/nithyashreek301-max/flask-ecs-cicd-lab.git',  // REPLACE THIS
                    credentialsId: 'github-token'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest
                """
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh """
                    trivy image \
                        --exit-code 1 \
                        --severity HIGH,CRITICAL \
                        --no-progress \
                        ${ECR_REPO}:${IMAGE_TAG}
                """
            }
            post {
                failure {
                    echo 'Trivy found HIGH or CRITICAL vulnerabilities — pipeline blocked. Fix the image before deploying.'
                }
            }
        }

        stage('Push to ECR') {
            steps {
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin \
                        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                """
            }
        }

        stage('Deploy to ECS') {
            steps {
                sh """
                    # Force ECS to pull the new image and restart tasks (rolling update)
                    aws ecs update-service \
                        --cluster ${ECS_CLUSTER} \
                        --service ${ECS_SERVICE} \
                        --force-new-deployment \
                        --region ${AWS_REGION}

                    # Wait until the new tasks are healthy and old ones are drained
                    aws ecs wait services-stable \
                        --cluster ${ECS_CLUSTER} \
                        --services ${ECS_SERVICE} \
                        --region ${AWS_REGION}
                """
            }
        }
    }

    post {
        success {
            echo "Deployment SUCCESS — image ${IMAGE_TAG} is live on ECS"
        }
        failure {
            echo "Pipeline FAILED — check the stage logs above for details"
        }
        always {
            // Clean up local Docker images to save disk space on Jenkins EC2
            sh """
                docker rmi ${ECR_REPO}:${IMAGE_TAG} || true
                docker rmi ${ECR_REPO}:latest || true
            """
        }
    }
}
