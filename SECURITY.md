# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| CVSS v3.0 | Supported Versions                        |
| --------- | ----------------------------------------- |
| 9.0-10.0  | Releases within the previous three months |
| 4.0-8.9   | Most recent release                       |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to **[security@agenttest.dev](mailto:nihal.srivastava05@gmail.com)** or create a private vulnerability report on GitHub. You will receive a response from us within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity but historically within a few days.

### What to Include

When reporting security issues, please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Possible impact of the vulnerability
- Any suggested fixes (if you have them)

### Security Best Practices for Users

- Keep AgentTest updated to the latest version
- Avoid putting sensitive data (API keys, passwords) directly in test files
- Use environment variables for sensitive configuration
- Be cautious when running tests with external API calls
- Review generated test code before running in production environments

## Security Features

AgentTest includes several security features:

- **Input validation** for all configuration files
- **Safe code execution** environments for test generation
- **No arbitrary code execution** from configuration files
- **Environment variable support** for sensitive data

## Responsible Disclosure

We kindly ask that you:

- Give us reasonable time to fix the issue before any disclosure
- Avoid privacy violations, destruction of data, and interruption or degradation of services
- Only interact with accounts you own or with explicit permission of the account holder

Thank you for helping keep AgentTest and our users safe!
