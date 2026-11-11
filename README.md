# CIS Benchmark Compliance Checker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

> **Automated CIS Benchmark compliance auditing and remediation tool for Ubuntu, RHEL, Amazon Linux, Windows Server, and macOS**

## Overview

CIS Benchmark Compliance Checker is a security automation tool that helps organizations maintain compliance with Center for Internet Security (CIS) benchmarks across multiple operating systems.

### Key Features

✅ **Multi-Platform Support**: Ubuntu, RHEL, Amazon Linux, Windows Server, macOS  
✅ **Automated Auditing**: Run hundreds of CIS benchmark checks in minutes  
✅ **Smart Remediation**: Fix non-compliant configurations with rollback support  
✅ **Rich Reporting**: Generate HTML, JSON, and CSV reports with interactive dashboards  
✅ **Customizable Profiles**: Adapt checks to your organizational requirements  
✅ **CI/CD Integration**: Easily integrate into automated pipelines  

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/SiteQ8/CIS-Benchmark-Compliance-Checker.git
cd CIS-Benchmark-Compliance-Checker

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py install
```

### Basic Usage

```bash
# Run a compliance audit
python -m cis_checker audit --os ubuntu --level 1

# Generate HTML report
python -m cis_checker report --format html --output ./reports

# Apply remediation (with backup)
python -m cis_checker remediate --profile ubuntu_22_04 --backup

# Dry run to see what would change
python -m cis_checker remediate --dry-run
```

## Supported Platforms

| Operating System | Versions | CIS Benchmark Version |
|-----------------|----------|----------------------|
| Ubuntu Linux | 20.04, 22.04, 24.04 | v1.0.0 - v2.0.0 |
| RHEL | 8, 9 | v2.0.0 - v3.0.0 |
| Amazon Linux | 2, 2023 | v3.0.0 |
| Windows Server | 2019, 2022 | v2.0.0 - v3.0.0 |
| macOS | 13, 14 | v4.0.0 - v5.0.0 |

## Security Categories Checked

1. **Initial Setup**: Filesystem, boot settings, mandatory access control
2. **Services**: System services, special purpose services, service clients
3. **Network Configuration**: Firewall, network parameters, protocol security
4. **Logging & Auditing**: System accounting, log configuration, audit rules
5. **Access Control**: PAM, SSH, user accounts, authentication
6. **System Maintenance**: File permissions, system file integrity

## Documentation

Documentation is available at: **https://siteq8.github.io/CIS-Benchmark-Compliance-Checker**

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## Security

Please report security vulnerabilities to site@hotmail.com. See [SECURITY.md](SECURITY.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: SiteQ8
- **Email**: site@hotmail.com
- **GitHub**: [@SiteQ8](https://github.com/SiteQ8)

---

**Disclaimer**: This tool is provided as-is for security assessment purposes. Always test in a non-production environment first.
