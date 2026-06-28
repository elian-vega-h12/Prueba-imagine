Feature: Docker and CI runtime

  Scenario: Start local runtime
    Given Docker is installed
    When the user runs "docker compose up"
    Then frontend, backend, PostgreSQL, and MongoDB services start
    And the backend applies database migrations before serving requests

  Scenario: Run CI checks
    Given code is pushed to GitHub
    When the GitHub Actions workflow runs
    Then backend dependencies are installed
    And frontend dependencies are installed
    And lint, tests, build, and mutation baseline commands run
