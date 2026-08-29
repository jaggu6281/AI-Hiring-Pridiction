// API Configuration - Auto-detect environment
const getAPIBaseURL = () => {
    // Local development
    if (
        window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1'
    ) {
        return 'http://localhost:8000';
    }

    // Production / deployed frontend
    return 'https://ai-hiring-pridiction-backend.onrender.com';
};
    
    // Production: same domain, use relative path
    // This works with both direct port access and reverse proxy
    if (window.location.hostname.includes('.')) {
        // For production, if backend is on same domain use it directly
        // Otherwise use the same domain at port 8000
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;
        const port = window.location.port;
        
        // If accessed via port 80/443 (standard ports), backend is likely on same domain
        if (!port || port === '80' || port === '443') {
            // Assume backend is proxied through same domain
            return `${protocol}//${hostname}`;
        }
        
        // If custom port, try to access backend on port 8000
        return `${protocol}//${hostname}:8000`;
    }
    
    // Fallback to current location
    return window.location.origin;
};

const API_BASE_URL = getAPIBaseURL();

// Debug: Log API URL
console.log('API Base URL:', API_BASE_URL);
console.log('Environment:', window.location.hostname);

// Status tracking
let apiConnected = false;
let healthCheckAttempts = 0;
const MAX_HEALTH_CHECK_ATTEMPTS = 6;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// Initialize app
async function initializeApp() {
    setupTabNavigation();
    checkAPIHealth();
    setupFormListeners();
}

// Check API health
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            mode: 'cors'
        });

        if (response.ok) {
            setAPIStatus(true);
            healthCheckAttempts = 0; // Reset on success
        } else {
            setAPIStatus(false);
            if (healthCheckAttempts < MAX_HEALTH_CHECK_ATTEMPTS) {
                healthCheckAttempts++;
                setTimeout(checkAPIHealth, 3000); // Retry after 3 seconds
            }
        }
    } catch (error) {
        console.error('API health check failed:', error);
        setAPIStatus(false);
        if (healthCheckAttempts < MAX_HEALTH_CHECK_ATTEMPTS) {
            healthCheckAttempts++;
            setTimeout(checkAPIHealth, 3000); // Retry after 3 seconds
        }
    }
}

// Set API status
function setAPIStatus(isOnline) {
    apiConnected = isOnline;
    const statusDot = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');

    if (isOnline) {
        statusDot.className = 'status-dot online';
        statusText.textContent = '✅ API Connected';
        statusText.style.color = 'var(--success-color)';
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = '❌ API Disconnected - Retrying...';
        statusText.style.color = 'var(--danger-color)';
    }
}

// Setup tab navigation
function setupTabNavigation() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Setup form listeners
function setupFormListeners() {
    document.getElementById('predictForm').addEventListener('submit', handlePredictSubmit);
    document.getElementById('jobFitForm').addEventListener('submit', handleJobFitSubmit);
    document.getElementById('reportForm').addEventListener('submit', handleReportSubmit);
}

// Handle predict form submit
async function handlePredictSubmit(e) {
    e.preventDefault();

    if (!apiConnected) {
        showError('predict', 'API is not connected. Please try again later.');
        return;
    }

    const name = document.getElementById('name').value;
    const jobRole = document.getElementById('jobRole').value;
    const skills = document.getElementById('skills').value;
    const experience = parseFloat(document.getElementById('experience').value);
    const education = document.getElementById('education').value;
    const projects = parseInt(document.getElementById('projects').value);
    const salary = parseFloat(document.getElementById('salary').value);
    const aiScore = parseFloat(document.getElementById('aiScore').value);
    const certifications = document.getElementById('certifications').value || "";

    if (!name || !jobRole || !skills || !experience || !education || !projects || !salary || !aiScore) {
        showError('predict', 'Please fill in all required fields.');
        return;
    }

    const resultBox = document.getElementById('predictResult');
    resultBox.innerHTML = '<div class="loading"></div> Processing...';
    resultBox.classList.remove('hidden');

    try {
        const payload = {
            Name: name,
            Job_Role: jobRole,
            Skills: skills,
            Experience_Years: experience,
            Education: education,
            Projects_Count: projects,
            Salary_Expectation: salary,
            AI_Score: aiScore,
            Certifications: certifications,
            Resume_ID: `CANDIDATE_${Date.now()}`
        };

        console.log('Sending payload:', payload);

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API error response:', errorData);
            throw new Error(`API error: ${response.statusText} - ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        displayPredictResult(data);
    } catch (error) {
        console.error('Prediction error:', error);
        showError('predict', `Error: ${error.message}`);
    }
}

// Handle job fit form submit
async function handleJobFitSubmit(e) {
    e.preventDefault();

    if (!apiConnected) {
        showError('job-fit', 'API is not connected. Please try again later.');
        return;
    }

    const name = document.getElementById('jobFitName').value;
    const jobRole = document.getElementById('jobFitRole').value;
    const skills = document.getElementById('jobFitSkills').value;
    const experience = parseFloat(document.getElementById('jobFitExperience').value);
    const education = document.getElementById('jobFitEducation').value;
    const projects = parseInt(document.getElementById('jobFitProjects').value);
    const salary = parseFloat(document.getElementById('jobFitSalary').value);
    const aiScore = parseFloat(document.getElementById('jobFitAIScore').value);

    if (!name || !jobRole || !skills || !experience || !education || !projects || !salary || !aiScore) {
        showError('job-fit', 'Please fill in all required fields.');
        return;
    }

    const resultBox = document.getElementById('jobFitResult');
    resultBox.innerHTML = '<div class="loading"></div> Analyzing fit...';
    resultBox.classList.remove('hidden');

    try {
        const payload = {
            Name: name,
            Job_Role: jobRole,
            Skills: skills,
            Experience_Years: experience,
            Education: education,
            Projects_Count: projects,
            Salary_Expectation: salary,
            AI_Score: aiScore,
            Certifications: "",
            Resume_ID: `CANDIDATE_${Date.now()}`
        };

        console.log('Sending job fit payload:', payload);

        const response = await fetch(`${API_BASE_URL}/job-fit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API error response:', errorData);
            throw new Error(`API error: ${response.statusText} - ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        displayJobFitResult(data);
    } catch (error) {
        console.error('Job fit error:', error);
        showError('job-fit', `Error: ${error.message}`);
    }
}

// Handle report form submit
async function handleReportSubmit(e) {
    e.preventDefault();

    if (!apiConnected) {
        showError('report', 'API is not connected. Please try again later.');
        return;
    }

    const name = document.getElementById('reportName').value;
    const jobRole = document.getElementById('reportRole').value;
    const skills = document.getElementById('reportSkills').value;
    const experience = parseFloat(document.getElementById('reportExperience').value);
    const education = document.getElementById('reportEducation').value;
    const projects = parseInt(document.getElementById('reportProjects').value);
    const salary = parseFloat(document.getElementById('reportSalary').value);
    const aiScore = parseFloat(document.getElementById('reportAIScore').value);

    if (!name || !jobRole || !skills || !experience || !education || !projects || !salary || !aiScore) {
        showError('report', 'Please fill in all required fields.');
        return;
    }

    const resultBox = document.getElementById('reportResult');
    resultBox.innerHTML = '<div class="loading"></div> Generating report...';
    resultBox.classList.remove('hidden');

    try {
        const payload = {
            Name: name,
            Job_Role: jobRole,
            Skills: skills,
            Experience_Years: experience,
            Education: education,
            Projects_Count: projects,
            Salary_Expectation: salary,
            AI_Score: aiScore,
            Certifications: "",
            Resume_ID: `CANDIDATE_${Date.now()}`
        };

        console.log('Sending report payload:', payload);

        const response = await fetch(`${API_BASE_URL}/candidate-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('API error response:', errorData);
            throw new Error(`API error: ${response.statusText} - ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        displayReportResult(data);
    } catch (error) {
        console.error('Report generation error:', error);
        showError('report', `Error: ${error.message}`);
    }
}

// Display predict result
function displayPredictResult(data) {
    const resultBox = document.getElementById('predictResult');
    const hireProbability = data.Hire_Probability || 0;
    const recommendation = data.Recommendation || 'No recommendation available';
    const name = data.Name || 'Candidate';
    const jobRole = data.Job_Role || 'Position';

    // Convert to percentage if it's between 0 and 1
    const probability = hireProbability > 1 ? hireProbability / 100 : hireProbability;
    const progressPercentage = Math.round(probability * 100);
    
    const isHired = probability >= 0.5;
    const resultClass = isHired ? 'success' : 'error';
    const icon = isHired ? '✅' : '❌';

    resultBox.className = `result-box ${resultClass}`;
    resultBox.innerHTML = `
        <div class="result-title">${icon} Prediction Result for ${name}</div>
        <div class="result-content">
            <div class="result-item">
                <span class="result-label">Position:</span>
                <span style="color: var(--text-dark);">${jobRole}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Outcome:</span>
                <span class="result-value">${isHired ? '✅ LIKELY TO BE HIRED' : '❌ LIKELY TO BE REJECTED'}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Hire Probability:</span>
                <span class="result-value">${progressPercentage}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progressPercentage}%">${progressPercentage}%</div>
            </div>
            <div class="result-item">
                <span class="result-label">Recommendation:</span>
                <span style="color: var(--text-dark);">${recommendation}</span>
            </div>
        </div>
    `;
}

// Display job fit result
function displayJobFitResult(data) {
    const resultBox = document.getElementById('jobFitResult');
    const fitScore = data.Job_Fit_Score || 0;
    const matchedSkills = data.Matched_Skills || [];
    const missingSkills = data.Missing_Skills || [];
    const jobRole = data.Job_Role || 'Position';

    const fitPercentage = Math.round(fitScore * 100);
    const fitClass = fitPercentage >= 70 ? 'success' : fitPercentage >= 50 ? 'warning' : 'error';
    const fitIcon = fitPercentage >= 70 ? '✅' : fitPercentage >= 50 ? '⚠️' : '❌';

    resultBox.className = `result-box ${fitClass}`;
    resultBox.innerHTML = `
        <div class="result-title">${fitIcon} Job Fit Analysis - ${jobRole}</div>
        <div class="result-content">
            <div class="result-item">
                <span class="result-label">Job Fit Score:</span>
                <span class="result-value">${fitPercentage}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${fitPercentage}%">${fitPercentage}%</div>
            </div>
            ${matchedSkills.length > 0 ? `
                <div style="padding: 0.75rem; background: #f0fdf4; border-radius: 0.5rem; border-left: 4px solid var(--success-color); margin-top: 1rem;">
                    <strong style="color: var(--success-color);">✓ Matching Skills (${matchedSkills.length}):</strong>
                    <div style="margin-top: 0.5rem;">${matchedSkills.join(', ')}</div>
                </div>
            ` : ''}
            ${missingSkills.length > 0 ? `
                <div style="padding: 0.75rem; background: #fef2f2; border-radius: 0.5rem; border-left: 4px solid var(--danger-color); margin-top: 1rem;">
                    <strong style="color: var(--danger-color);">✗ Missing Skills (${missingSkills.length}):</strong>
                    <div style="margin-top: 0.5rem;">${missingSkills.join(', ')}</div>
                </div>
            ` : ''}
            <div class="result-item" style="margin-top: 1rem;">
                <span class="result-label">Assessment:</span>
                <span style="color: var(--text-dark);">
                    ${fitPercentage >= 80 ? '🚀 Excellent fit for this role!' : 
                      fitPercentage >= 60 ? '👍 Good fit with some skill gaps' : 
                      'ℹ️ Consider upskilling before applying'}
                </span>
            </div>
        </div>
    `;
}

// Display report result
function displayReportResult(data) {
    const resultBox = document.getElementById('reportResult');
    const candidateName = data.Name || 'Candidate';
    const jobRole = data.Job_Role || 'Position';
    const hireProbability = data.Hire_Probability || 0;
    const jobFitScore = data.Job_Fit_Score || 0;
    const candidateStrengthScore = data.Candidate_Strength_Score || 0;
    const recruitmentScore = data.Recruitment_Score || 0;
    const recommendation = data.Recommendation || 'Requires further evaluation';
    const matchedSkills = data.Matched_Skills || [];
    const missingSkills = data.Missing_Skills || [];
    const positiveFactors = data.Positive_Model_Factors || [];
    const negativeFactors = data.Negative_Model_Factors || [];

    // Convert scores to percentages
    const hirePct = Math.round((hireProbability > 1 ? hireProbability / 100 : hireProbability) * 100);
    const fitPct = Math.round((jobFitScore > 1 ? jobFitScore / 100 : jobFitScore) * 100);
    const strengthPct = Math.round((candidateStrengthScore > 1 ? candidateStrengthScore / 100 : candidateStrengthScore) * 100);
    const recruitmentPct = Math.round((recruitmentScore > 1 ? recruitmentScore / 100 : recruitmentScore) * 100);

    const overallScore = Math.round((hirePct + fitPct + strengthPct + recruitmentPct) / 4);
    const resultClass = overallScore >= 70 ? 'success' : overallScore >= 50 ? 'warning' : 'error';

    resultBox.className = `result-box ${resultClass}`;
    resultBox.innerHTML = `
        <div class="result-title">📄 Comprehensive Candidate Report - ${candidateName}</div>
        <div class="result-content">
            <div class="result-item">
                <span class="result-label">Position Applied:</span>
                <span style="color: var(--text-dark);">${jobRole}</span>
            </div>
            <div class="result-item">
                <span class="result-label">Overall Score:</span>
                <span class="result-value">${overallScore}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${overallScore}%">${overallScore}%</div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="padding: 1rem; background: #f3f4f6; border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                    <strong>Hire Probability</strong>
                    <div style="font-size: 1.5rem; color: var(--primary-color); margin-top: 0.5rem;">${hirePct}%</div>
                </div>
                <div style="padding: 1rem; background: #f3f4f6; border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                    <strong>Job Fit Score</strong>
                    <div style="font-size: 1.5rem; color: var(--primary-color); margin-top: 0.5rem;">${fitPct}%</div>
                </div>
                <div style="padding: 1rem; background: #f3f4f6; border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                    <strong>Candidate Strength</strong>
                    <div style="font-size: 1.5rem; color: var(--primary-color); margin-top: 0.5rem;">${strengthPct}%</div>
                </div>
                <div style="padding: 1rem; background: #f3f4f6; border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                    <strong>Recruitment Score</strong>
                    <div style="font-size: 1.5rem; color: var(--primary-color); margin-top: 0.5rem;">${recruitmentPct}%</div>
                </div>
            </div>

            ${matchedSkills.length > 0 ? `
                <div style="padding: 0.75rem; background: #f0fdf4; border-radius: 0.5rem; border-left: 4px solid var(--success-color); margin-top: 1rem;">
                    <strong style="color: var(--success-color);">✓ Matched Skills (${matchedSkills.length}):</strong>
                    <div style="margin-top: 0.5rem;">${matchedSkills.join(', ')}</div>
                </div>
            ` : ''}

            ${missingSkills.length > 0 ? `
                <div style="padding: 0.75rem; background: #fef2f2; border-radius: 0.5rem; border-left: 4px solid var(--danger-color); margin-top: 1rem;">
                    <strong style="color: var(--danger-color);">✗ Missing Skills (${missingSkills.length}):</strong>
                    <div style="margin-top: 0.5rem;">${missingSkills.join(', ')}</div>
                </div>
            ` : ''}

            ${positiveFactors.length > 0 ? `
                <div style="padding: 0.75rem; background: #f0fdf4; border-radius: 0.5rem; border-left: 4px solid var(--success-color); margin-top: 1rem;">
                    <strong style="color: var(--success-color);">💪 Positive Factors:</strong>
                    <ul style="margin-left: 1rem; margin-top: 0.5rem;">
                        ${positiveFactors.map(f => `<li>${f}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}

            ${negativeFactors.length > 0 ? `
                <div style="padding: 0.75rem; background: #fffbeb; border-radius: 0.5rem; border-left: 4px solid var(--warning-color); margin-top: 1rem;">
                    <strong style="color: var(--warning-color);">⚠️ Areas for Development:</strong>
                    <ul style="margin-left: 1rem; margin-top: 0.5rem;">
                        ${negativeFactors.map(f => `<li>${f}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}

            <div class="result-item" style="margin-top: 1rem;">
                <span class="result-label">Recommendation:</span>
                <span style="color: var(--text-dark); font-size: 1.05rem;">${recommendation}</span>
            </div>
        </div>
    `;
}

// Show error message
function showError(tabName, message) {
    const resultBox = document.getElementById(`${tabName}Result`);
    resultBox.className = 'result-box error';
    resultBox.innerHTML = `
        <div class="result-title">❌ Error</div>
        <div class="result-content">
            <p style="color: var(--danger-color);">${message}</p>
        </div>
    `;
    resultBox.classList.remove('hidden');
}
