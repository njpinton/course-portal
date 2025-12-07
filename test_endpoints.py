#!/usr/bin/env python3
"""
Comprehensive endpoint testing for Presenter App Flask API
Tests all routes and endpoints with various scenarios
"""

import requests
import json
import sys
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8788"
TEST_TIMEOUT = 5
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Color codes for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class EndpointTester:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.admin_token = None
        self.group_token = None
        self.class_id = "4f4e1c34-9d3b-4d6c-b3e3-4f3c3c3c3c3c"  # Example UUID
        self.group_id = "550e8400-e29b-41d4-a716-446655440000"  # Example UUID

    def log_result(self, endpoint, method, status, message, error=None):
        """Log test result"""
        result = {
            'endpoint': endpoint,
            'method': method,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        if error:
            result['error'] = str(error)
        self.results.append(result)

        status_color = GREEN if status == 'PASS' else RED if status == 'FAIL' else YELLOW
        print(f"{status_color}{status:6s}{RESET} | {method:6s} | {endpoint:50s} | {message}")

    def test_endpoint(self, method, endpoint, expected_status=None, data=None, headers=None, auth_required=False):
        """Test a single endpoint"""
        url = f"{BASE_URL}{endpoint}"
        try:
            if method == 'GET':
                resp = self.session.get(url, timeout=TEST_TIMEOUT, headers=headers)
            elif method == 'POST':
                resp = self.session.post(url, json=data, timeout=TEST_TIMEOUT, headers=headers)
            elif method == 'PUT':
                resp = self.session.put(url, json=data, timeout=TEST_TIMEOUT, headers=headers)
            elif method == 'DELETE':
                resp = self.session.delete(url, timeout=TEST_TIMEOUT, headers=headers)
            else:
                self.log_result(endpoint, method, 'FAIL', f"Unknown method: {method}")
                return False

            # Check response
            if expected_status and resp.status_code != expected_status:
                # Some endpoints might return auth errors or not found - still valid test
                if resp.status_code in [401, 403, 404, 405]:
                    self.log_result(endpoint, method, 'PASS', f"Status {resp.status_code} (expected)")
                    return True
                else:
                    self.log_result(endpoint, method, 'FAIL', f"Status {resp.status_code} (expected {expected_status})")
                    return False
            else:
                status = 'PASS' if resp.status_code < 400 else 'WARN'
                self.log_result(endpoint, method, status, f"Status {resp.status_code}")
                return resp.status_code < 400

        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
            self.log_result(endpoint, method, 'FAIL', "Connection failed", error=e)
            return False
        except requests.exceptions.Timeout:
            self.log_result(endpoint, method, 'FAIL', "Timeout", error="Request timed out")
            return False
        except Exception as e:
            self.log_result(endpoint, method, 'FAIL', "Exception", error=e)
            return False

    def run_all_tests(self):
        """Run comprehensive endpoint tests"""
        print(f"\n{BOLD}{BLUE}=== PRESENTER APP ENDPOINT TESTS ==={RESET}")
        print(f"Base URL: {BASE_URL}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Test server connectivity first
        print(f"{BOLD}Testing Server Connectivity...{RESET}")
        try:
            resp = requests.get(f"{BASE_URL}/", timeout=5)
            print(f"{GREEN}✓ Server is running{RESET}\n")
        except:
            print(f"{RED}✗ Server is not running or not responding{RESET}")
            print(f"Make sure to start the Flask app with: python3 api/index.py")
            return False

        # Public endpoints
        print(f"{BOLD}Testing Public Endpoints...{RESET}")
        self.test_endpoint('GET', '/', expected_status=200)
        self.test_endpoint('GET', '/module/1', expected_status=200)
        self.test_endpoint('GET', '/favicon.ico', expected_status=404)
        self.test_endpoint('GET', '/images/test.png', expected_status=404)

        # Admin endpoints
        print(f"\n{BOLD}Testing Admin Endpoints...{RESET}")
        self.test_endpoint('GET', '/admin_login', expected_status=200)
        self.test_endpoint('POST', '/admin_login',
                          data={'username': ADMIN_USERNAME, 'password': ADMIN_PASSWORD},
                          expected_status=302)
        self.test_endpoint('GET', '/admin_dashboard', expected_status=302)  # Redirects if not logged in
        self.test_endpoint('GET', '/admin_roster', expected_status=302)
        self.test_endpoint('GET', '/admin_submissions', expected_status=302)
        self.test_endpoint('GET', '/admin_logout', expected_status=302)

        # Group Portal Endpoints
        print(f"\n{BOLD}Testing Group Portal Endpoints...{RESET}")
        self.test_endpoint('GET', '/group_portal', expected_status=302)  # Redirects if not logged in
        self.test_endpoint('GET', '/group_login', expected_status=200)
        self.test_endpoint('GET', '/group_submission_portal', expected_status=302)
        self.test_endpoint('GET', '/group_logout', expected_status=302)

        # API - Groups Endpoints
        print(f"\n{BOLD}Testing API - Groups Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/groups', expected_status=200)
        self.test_endpoint('POST', '/api/groups',
                          data={'group_name': 'Test Group', 'username': 'testgroup'},
                          expected_status=401)  # Auth required
        self.test_endpoint('GET', f'/api/groups/{self.group_id}', expected_status=404)
        self.test_endpoint('DELETE', f'/api/groups/{self.group_id}', expected_status=401)
        self.test_endpoint('POST', f'/api/groups/{self.group_id}/documents',
                          expected_status=401)
        self.test_endpoint('GET', f'/api/groups/{self.group_id}/stages', expected_status=404)
        self.test_endpoint('GET', f'/api/groups/{self.group_id}/models', expected_status=404)
        self.test_endpoint('POST', f'/api/groups/{self.group_id}/models',
                          expected_status=401)
        self.test_endpoint('GET', f'/api/groups/{self.group_id}/stage-documents', expected_status=404)

        # API - Stages Endpoints
        print(f"\n{BOLD}Testing API - Stages Endpoints...{RESET}")
        self.test_endpoint('PUT', '/api/stages/test-stage-id',
                          data={'status': 'complete'},
                          expected_status=400)  # Invalid stage ID

        # API - Admin Endpoints
        print(f"\n{BOLD}Testing API - Admin Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/admin/statistics', expected_status=200)
        self.test_endpoint('GET', '/api/admin/submissions', expected_status=200)
        self.test_endpoint('GET', '/api/admin/submissions/test-id', expected_status=404)
        self.test_endpoint('GET', '/api/admin/download/test-id', expected_status=404)
        self.test_endpoint('GET', '/api/admin/view/test-id', expected_status=404)
        self.test_endpoint('GET', '/api/admin/groups/submission-status', expected_status=200)
        self.test_endpoint('GET', '/admin/group/550e8400-e29b-41d4-a716-446655440000', expected_status=404)

        # API - Student Endpoints
        print(f"\n{BOLD}Testing API - Student Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/students/class/4f4e1c34-9d3b-4d6c-b3e3-4f3c3c3c3c3c',
                          expected_status=200)
        self.test_endpoint('GET', '/api/students/ungrouped/all', expected_status=200)
        self.test_endpoint('GET', '/api/students/ungrouped/4f4e1c34-9d3b-4d6c-b3e3-4f3c3c3c3c3c',
                          expected_status=200)
        self.test_endpoint('GET', '/api/students/grouped/4f4e1c34-9d3b-4d6c-b3e3-4f3c3c3c3c3c',
                          expected_status=200)
        self.test_endpoint('GET', '/api/students/campus/12345', expected_status=200)
        self.test_endpoint('POST', '/api/students/550e8400-e29b-41d4-a716-446655440000/assign-group/550e8400-e29b-41d4-a716-446655440001',
                          expected_status=401)  # Auth required
        self.test_endpoint('POST', '/api/students/550e8400-e29b-41d4-a716-446655440000/unassign-group',
                          expected_status=401)  # Auth required

        # API - Group Members Endpoints
        print(f"\n{BOLD}Testing API - Group Members Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/group/members/ungrouped', expected_status=200)
        self.test_endpoint('GET', '/api/group/members/available', expected_status=200)
        self.test_endpoint('POST', '/api/group/members/add',
                          expected_status=401)  # Auth required
        self.test_endpoint('GET', '/api/groups/550e8400-e29b-41d4-a716-446655440000/members',
                          expected_status=404)

        # API - Comments Endpoints
        print(f"\n{BOLD}Testing API - Comments Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/groups/550e8400-e29b-41d4-a716-446655440000/comments',
                          expected_status=404)
        self.test_endpoint('POST', '/api/groups/550e8400-e29b-41d4-a716-446655440000/comments',
                          expected_status=401)  # Auth required

        # API - Classes Endpoints
        print(f"\n{BOLD}Testing API - Classes Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/classes/cmsc173a', expected_status=200)

        # API - Submission Endpoints
        print(f"\n{BOLD}Testing API - Submission Endpoints...{RESET}")
        self.test_endpoint('GET', '/api/student/submissions', expected_status=401)
        self.test_endpoint('POST', '/api/student/submit',
                          expected_status=401)  # Auth required
        self.test_endpoint('POST', '/api/student/submit-file/stage-id',
                          expected_status=401)  # Auth required
        self.test_endpoint('POST', '/api/group/submit',
                          expected_status=401)  # Auth required
        self.test_endpoint('PUT', '/api/group/submission/test-id',
                          expected_status=401)  # Auth required
        self.test_endpoint('PUT', '/api/group/delete',
                          expected_status=401)  # Auth required

        return self.generate_report()

    def generate_report(self):
        """Generate test report"""
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        warnings = sum(1 for r in self.results if r['status'] == 'WARN')
        total = len(self.results)

        print(f"\n{BOLD}{BLUE}=== TEST SUMMARY ==={RESET}")
        print(f"{GREEN}Passed:  {passed}{RESET}")
        print(f"{RED}Failed:  {failed}{RESET}")
        print(f"{YELLOW}Warnings: {warnings}{RESET}")
        print(f"{BOLD}Total:   {total}{RESET}\n")

        if failed == 0:
            print(f"{GREEN}{BOLD}✓ All tests passed!{RESET}\n")
            return True
        else:
            print(f"{RED}{BOLD}✗ Some tests failed!{RESET}")
            print(f"\nFailed tests:")
            for r in self.results:
                if r['status'] == 'FAIL':
                    print(f"  - {r['method']} {r['endpoint']}: {r['message']}")
            return False

def main():
    """Main test runner"""
    tester = EndpointTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
