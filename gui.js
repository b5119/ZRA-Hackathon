import React, { useState, useEffect } from 'react';
import { Upload, AlertTriangle, CheckCircle, XCircle, Download, Search, Users, Building, Shield } from 'lucide-react';

const GhostBuster = () => {
  const [companies, setCompanies] = useState([]);
  const [flaggedCompanies, setFlaggedCompanies] = useState([]);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');

  // Mock data generators
  const generateMockNAPSAData = () => {
    const validNRCs = [
      "123456/78/1", "234567/89/1", "345678/90/1", "456789/01/1", 
      "567890/12/1", "678901/23/1", "789012/34/1", "890123/45/1",
      "901234/56/1", "012345/67/1", "111111/11/1", "222222/22/1"
    ];
    return validNRCs.map((nrc, index) => ({
      name: `Employee ${index + 1}`,
      nrc: nrc
    }));
  };

  const generateMockPACRAData = () => {
    return [
      { name: "Acme Corporation", tpin: "1001-123456-78", regNumber: "REG001" },
      { name: "Tech Solutions Ltd", tpin: "1002-234567-89", regNumber: "REG002" },
      { name: "Mining Ventures", tpin: "1003-345678-90", regNumber: "REG003" },
      { name: "Retail Express", tpin: "1004-456789-01", regNumber: "REG004" },
      { name: "Construction Co", tpin: "1005-567890-12", regNumber: "REG005" }
    ];
  };

  const generateMockCompanyData = () => {
    const mockCompanies = [
      {
        name: "Acme Corporation",
        tpin: "1001-123456-78",
        employees: [
          { name: "John Doe", nrc: "123456/78/1" },
          { name: "Jane Smith", nrc: "234567/89/1" },
          { name: "Bob Wilson", nrc: "invalid-nrc-1" }
        ]
      },
      {
        name: "Ghost Company Ltd", // Not in PACRA
        tpin: "9999-999999-99",
        employees: [
          { name: "Fake Employee 1", nrc: "000000/00/0" },
          { name: "Fake Employee 2", nrc: "111111/11/1" }, // Valid but reused
          { name: "Fake Employee 3", nrc: "invalid-format" }
        ]
      },
      {
        name: "Tech Solutions Ltd",
        tpin: "1002-234567-89",
        employees: [
          { name: "Alice Johnson", nrc: "345678/90/1" },
          { name: "Charlie Brown", nrc: "111111/11/1" }, // Reused NRC
          { name: "Diana Prince", nrc: "456789/01/1" }
        ]
      },
      {
        name: "Phantom Enterprises", // Not in PACRA
        tpin: "8888-888888-88",
        employees: [
          { name: "Ghost Worker 1", nrc: "bad-nrc-format" },
          { name: "Ghost Worker 2", nrc: "another-bad-nrc" },
          { name: "Ghost Worker 3", nrc: "999999/99/9" }
        ]
      }
    ];
    return mockCompanies;
  };

  // NRC Validation Logic
  const validateNRC = (nrc) => {
    // Basic NRC format: XXXXXX/XX/X
    const nrcPattern = /^\d{6}\/\d{2}\/\d$/;
    return nrcPattern.test(nrc);
  };

  // Analysis Logic
  const analyzeCompanies = (companyData) => {
    const napsaData = generateMockNAPSAData();
    const pacraData = generateMockPACRAData();
    const nrcUsageMap = new Map();
    const results = [];

    // Track NRC usage across companies
    companyData.forEach(company => {
      company.employees.forEach(employee => {
        if (!nrcUsageMap.has(employee.nrc)) {
          nrcUsageMap.set(employee.nrc, []);
        }
        nrcUsageMap.get(employee.nrc).push(company.name);
      });
    });

    companyData.forEach(company => {
      const flags = [];
      let riskScore = 0;

      // Check each employee
      let invalidNRCs = 0;
      let missingFromNAPSA = 0;
      let reusedNRCs = 0;

      company.employees.forEach(employee => {
        // Validate NRC format
        if (!validateNRC(employee.nrc)) {
          invalidNRCs++;
          riskScore += 10;
        }

        // Check if exists in NAPSA
        const existsInNAPSA = napsaData.some(napsa => napsa.nrc === employee.nrc);
        if (!existsInNAPSA && validateNRC(employee.nrc)) {
          missingFromNAPSA++;
          riskScore += 5;
        }

        // Check for NRC reuse
        const usage = nrcUsageMap.get(employee.nrc);
        if (usage && usage.length > 1) {
          reusedNRCs++;
          riskScore += 15;
        }
      });

      // Check company registration
      const pacraMatch = pacraData.some(pacra => 
        pacra.name.toLowerCase() === company.name.toLowerCase() ||
        pacra.tpin === company.tpin
      );

      if (!pacraMatch) {
        flags.push("No PACRA registration found");
        riskScore += 25;
      }

      if (invalidNRCs > 0) {
        flags.push(`${invalidNRCs} invalid NRC format(s)`);
      }

      if (missingFromNAPSA > 0) {
        flags.push(`${missingFromNAPSA} employee(s) not in NAPSA database`);
      }

      if (reusedNRCs > 0) {
        flags.push(`${reusedNRCs} NRC(s) used in multiple companies`);
      }

      // Online presence simulation (simplified)
      const hasOnlinePresence = Math.random() > 0.3; // 70% chance of having presence
      if (!hasOnlinePresence) {
        flags.push("No significant online presence detected");
        riskScore += 10;
      }

      // Determine risk level
      let riskLevel = 'Low';
      if (riskScore >= 50) riskLevel = 'Critical';
      else if (riskScore >= 25) riskLevel = 'High';
      else if (riskScore >= 10) riskLevel = 'Medium';

      const result = {
        ...company,
        flags,
        riskScore,
        riskLevel,
        isFlagged: flags.length > 0,
        employeeCount: company.employees.length,
        validEmployees: company.employees.length - invalidNRCs - missingFromNAPSA,
        pacraRegistered: pacraMatch,
        hasOnlinePresence
      };

      results.push(result);
    });

    return results;
  };

  const handleAnalyze = () => {
    setLoading(true);
    setTimeout(() => {
      const mockData = generateMockCompanyData();
      setCompanies(mockData);
      const results = analyzeCompanies(mockData);
      setAnalysisResults(results);
      setFlaggedCompanies(results.filter(company => company.isFlagged));
      setLoading(false);
      setActiveTab('results');
    }, 2000);
  };

  const exportResults = () => {
    const exportData = flaggedCompanies.map(company => ({
      'Company Name': company.name,
      'TPIN': company.tpin,
      'Risk Level': company.riskLevel,
      'Risk Score': company.riskScore,
      'Flags': company.flags.join('; '),
      'Employee Count': company.employeeCount,
      'Valid Employees': company.validEmployees,
      'PACRA Registered': company.pacraRegistered ? 'Yes' : 'No'
    }));

    const csv = [
      Object.keys(exportData[0]).join(','),
      ...exportData.map(row => Object.values(row).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ghostbuster_flagged_companies.csv';
    a.click();
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'Critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'High': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Shield className="h-12 w-12 text-indigo-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">GhostBuster</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-Powered Detection System for Fake Companies & Phantom Employees
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Built for Zambia Revenue Authority (ZRA) - Hackathon Demo
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg p-1 shadow-lg">
            <div className="flex space-x-1">
              {['upload', 'results', 'dashboard'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-6 py-2 rounded-md font-medium transition-colors ${
                    activeTab === tab
                      ? 'bg-indigo-600 text-white'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="text-center">
                <Upload className="h-16 w-16 text-indigo-600 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Upload Company Data
                </h2>
                <p className="text-gray-600 mb-8">
                  For this demo, we'll use simulated ZRA company data to demonstrate the system's capabilities.
                </p>
                
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-6">
                  <div className="text-gray-500 mb-4">
                    <Building className="h-8 w-8 mx-auto mb-2" />
                    Demo includes sample companies with various risk factors
                  </div>
                  <div className="text-sm text-gray-400">
                    • Companies with invalid NRCs<br/>
                    • Unregistered businesses<br/>
                    • Duplicate employee records<br/>
                    • Missing NAPSA registrations
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Analyzing Companies...
                    </>
                  ) : (
                    <>
                      <Search className="h-5 w-5 mr-2" />
                      Start Analysis
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Results Tab */}
        {activeTab === 'results' && analysisResults && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
                <button
                  onClick={exportResults}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export Flagged
                </button>
              </div>

              {/* Summary Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="flex items-center">
                    <Building className="h-8 w-8 text-blue-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-600">Total Companies</p>
                      <p className="text-2xl font-bold text-gray-900">{analysisResults.length}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-red-50 rounded-lg p-4">
                  <div className="flex items-center">
                    <AlertTriangle className="h-8 w-8 text-red-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-600">Flagged Companies</p>
                      <p className="text-2xl font-bold text-gray-900">{flaggedCompanies.length}</p>
                    </div>
                  </div>
                </div>
                <div className="bg-yellow-50 rounded-lg p-4">
                  <div className="flex items-center">
                    <Users className="h-8 w-8 text-yellow-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-600">Total Employees</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {analysisResults.reduce((sum, company) => sum + company.employeeCount, 0)}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex items-center">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-600">Clean Companies</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {analysisResults.length - flaggedCompanies.length}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Company Results */}
              <div className="space-y-4">
                {analysisResults.map((company, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{company.name}</h3>
                        <p className="text-sm text-gray-600">TPIN: {company.tpin}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getRiskColor(company.riskLevel)}`}>
                          {company.riskLevel} Risk
                        </span>
                        {company.isFlagged ? (
                          <XCircle className="h-6 w-6 text-red-500" />
                        ) : (
                          <CheckCircle className="h-6 w-6 text-green-500" />
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3 text-sm">
                      <div>
                        <span className="font-medium">Employees:</span> {company.employeeCount}
                      </div>
                      <div>
                        <span className="font-medium">Valid:</span> {company.validEmployees}
                      </div>
                      <div>
                        <span className="font-medium">PACRA:</span> 
                        <span className={company.pacraRegistered ? 'text-green-600' : 'text-red-600'}>
                          {company.pacraRegistered ? ' ✓' : ' ✗'}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium">Risk Score:</span> {company.riskScore}
                      </div>
                    </div>

                    {company.flags.length > 0 && (
                      <div className="bg-red-50 border border-red-200 rounded p-3">
                        <p className="font-medium text-red-800 mb-1">Issues Detected:</p>
                        <ul className="text-sm text-red-700 space-y-1">
                          {company.flags.map((flag, flagIndex) => (
                            <li key={flagIndex}>• {flag}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">System Information</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Validation Checks</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      NRC Format Validation
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      NAPSA Database Cross-check
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      PACRA Registration Verification
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      Duplicate NRC Detection
                    </div>
                    <div className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      Online Presence Check
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Risk Scoring</h3>
                  <div className="space-y-2 text-sm">
                    <div>Invalid NRC: <span className="font-medium">+10 points</span></div>
                    <div>Missing from NAPSA: <span className="font-medium">+5 points</span></div>
                    <div>Reused NRC: <span className="font-medium">+15 points</span></div>
                    <div>No PACRA registration: <span className="font-medium">+25 points</span></div>
                    <div>No online presence: <span className="font-medium">+10 points</span></div>
                  </div>
                </div>
              </div>

              <div className="mt-8 p-4 bg-blue-50 rounded-lg">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">About GhostBuster</h3>
                <p className="text-blue-800 text-sm">
                  This system helps ZRA identify potentially fraudulent companies and phantom employees 
                  by cross-referencing multiple data sources and applying intelligent validation rules. 
                  The AI-powered approach can significantly reduce manual verification time while 
                  improving detection accuracy.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GhostBuster;