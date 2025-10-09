## TP1 - SAST & SCA
- Build the Docker image:
  ```bash
  docker build -t tp-security-app .
  ```
- Install Bandit:
  ```bash
  pip install bandit
  ```
- Run a Bandit scan:
  ```bash
  bandit -r .
  ```
- Findings addressed:
  - Replaced unsafe `eval` usage with a restricted AST evaluator.
  - Switched from `os.system` to an allowlisted `subprocess.run` call.
- **Recommended:** Use Snyk CLI for SCA:
  ```bash
  # Download from https://github.com/snyk/cli/releases
  # Or use npm: npm install -g snyk
  snyk auth
  snyk test
  ```
- Alternative: Use Safety (Python-specific):
  ```bash
  pip install safety
  safety check --file requirements.txt
  ```
  safety check --file requirements.txt
- **SCA Findings (Snyk):**
  - **Before fix:** Flask==2.0.1, Werkzeug==2.0.3 (7 vulnerabilities: DoS, RCE, Directory Traversal)
  - **After fix:** Flask==3.0.3, Werkzeug==3.0.6
  - **Why needed:** Fixes critical RCE and high-severity DoS vulnerabilities in Werkzeug
- Verify fix:
  ```bash
  pip install -r requirements.txt
  .\snyk-win.exe test
  ```
- Run Flask app (contains SQL injection & XSS vulnerabilities):
  ```bash
  python app.py
  ```
  python app.py
  ```
