#!/bin/bash
# Ubuntu CIS Benchmark Checks
# Author: SiteQ8
# Description: Bash-based compliance checks for Ubuntu Linux

echo "=== Ubuntu CIS Benchmark Compliance Checks ==="
echo ""

# 1.1.1 - Check cramfs filesystem
echo "[1.1.1] Checking cramfs filesystem..."
if lsmod | grep -q cramfs; then
    echo "❌ FAIL: cramfs is loaded"
else
    echo "✅ PASS: cramfs is not loaded"
fi

# 3.5.1.1 - Check UFW status
echo "[3.5.1.1] Checking UFW firewall..."
if ufw status | grep -q "Status: active"; then
    echo "✅ PASS: UFW is active"
else
    echo "❌ FAIL: UFW is not active"
fi

# 4.1.1.1 - Check auditd
echo "[4.1.1.1] Checking auditd installation..."
if dpkg -s auditd &>/dev/null; then
    echo "✅ PASS: auditd is installed"
else
    echo "❌ FAIL: auditd is not installed"
fi

# 5.4.1.1 - Check password expiration
echo "[5.4.1.1] Checking password expiration..."
max_days=$(grep "^PASS_MAX_DAYS" /etc/login.defs | awk '{print $2}')
if [ "$max_days" -le 365 ] && [ "$max_days" -gt 0 ]; then
    echo "✅ PASS: Password expiration is $max_days days"
else
    echo "❌ FAIL: Password expiration is $max_days days (should be ≤365)"
fi

# 6.1.2 - Check /etc/shadow permissions
echo "[6.1.2] Checking /etc/shadow permissions..."
perms=$(stat -c %a /etc/shadow)
if [ "$perms" = "000" ] || [ "$perms" = "600" ]; then
    echo "✅ PASS: /etc/shadow has correct permissions ($perms)"
else
    echo "❌ FAIL: /etc/shadow has incorrect permissions ($perms)"
fi

echo ""
echo "=== Compliance Check Completed ==="
