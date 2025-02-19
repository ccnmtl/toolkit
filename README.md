# Toolkit
Managed by Columbia University's Center for Teaching and Learning to host various independent web tools for small projects that do not require their own infrastsructure.

## Local Devlopment
### Prerequisites
* Docker
* Git

### Steps
1. In your terminal, change your directory to wherever you would like your test environment.
2. Run the following code to download the repository into your local directory:
   ```
   git clone git@github.com:ccnmtl/toolkit.git
   ```
3. Change to the newly created `toolkit` directory.
4. Make sure Docker is up and running and that port 8000 is available.
5. Run the following to start the site:
   ```
   docker compose up
   ```
   * You will see the docker logs in the terminal.
6. From your web browser you can now visit the site from `localhost:8000`.

## Staging and Production Development
Environemnt variables are defined in Jenkinsfile lines [31:40]. In the base build parameters are stored in Amaozn Web Services and fetched into the environment variables. Access to the parameter store is stored in the Jenkins configuration.

If you are not using AWS you will need to replace, at minimum, all of the lines that call `getAwsParameter()` with another secure parameter store. 

*Be careful not to expose any sensitive data.*

The following parameters need to be replaced unless you replicate the default backend.
```
jobsDbHost
jobsDbUser
jobsDbPassword
jobsDbPort
SENTRY_DSN -- only if you are using Sentry to track errors
SENTRY_KEY -- only if you are using Sentry to track errors
```

## Included tools
* [Aboelela](https://toolkit.ctl.columbia.edu/aboelela/) - A data processor for Dr. Sally Aboelela's *Generative AI to Close Learning Gaps*
