document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded.');
    const transactionForm = document.getElementById('transaction_form');
    const messageParagraph = document.getElementById('message');

    const navLinks = document.querySelectorAll('.sidebar ul li a');
    const contentSections = document.querySelectorAll('.content-section');

    // Chart instances
    let portfolioValueChartInstance = null;
    let dailyPnlChartInstance = null;
    let assetAllocationChartInstance = null;
    let twrChartInstance = null;
    let cumulativeReturnChartInstance = null;

    // DataTable instances
    let portfolioValueTableInstance = null;
    let openPositionsTableInstance = null;
    let closedPositionsTableInstance = null;

    // Chart tab elements
    const chartTabs = document.querySelectorAll('.chart-tab-button');
    const chartContents = document.querySelectorAll('.chart-tab-content');
    console.log('chartTabs (buttons):', chartTabs);
    console.log('chartContents (divs):', chartContents);

    function showSection(sectionId) {
        contentSections.forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(sectionId).classList.remove('hidden');
    }

    function setActiveLink(activeId) {
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        document.getElementById(activeId).classList.add('active');
    }

    // --- Individual Chart Rendering Functions ---
    async function renderPortfolioValueChart() {
        console.log('Rendering Portfolio Value Chart...');
        if (portfolioValueChartInstance) portfolioValueChartInstance.destroy();
        const portfolioValueData = await fetch('/data/chart/portfolio_value_over_time').then(res => res.json());
        console.log('Portfolio Value Data:', portfolioValueData);
        const ctx = document.getElementById('portfolio_value_chart').getContext('2d');
        console.log('Portfolio Value Chart Context:', ctx);
        portfolioValueChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: portfolioValueData.dates,
                datasets: [
                    {
                        label: 'Total Portfolio Value',
                        data: portfolioValueData.current_value,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1,
                        fill: false
                    },
                    {
                        label: 'Total Cost',
                        data: portfolioValueData.cost,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true, // Allow chart to fill container
                plugins: {
                    title: {
                        display: true,
                        text: 'Portfolio Value Over Time',
                        color: '#ffffff'
                    },
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    async function renderDailyPnlChart() {
        console.log('Rendering Daily P&L Chart...');
        if (dailyPnlChartInstance) dailyPnlChartInstance.destroy();
        const dailyPnlData = await fetch('/data/chart/daily_pnl_change').then(res => res.json());
        console.log('Daily P&L Data:', dailyPnlData);
        const ctx = document.getElementById('daily_pnl_chart').getContext('2d');
        console.log('Daily P&L Chart Context:', ctx);
        dailyPnlChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dailyPnlData.dates,
                datasets: [
                    {
                        label: 'Daily P&L Change',
                        data: dailyPnlData.daily_pnl_change,
                        backgroundColor: dailyPnlData.daily_pnl_change.map(value => value > 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)'),
                        borderColor: dailyPnlData.daily_pnl_change.map(value => value > 0 ? 'rgb(75, 192, 192)' : 'rgb(255, 99, 132)'),
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Daily P&L Change',
                        color: '#ffffff'
                    },
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    async function renderAssetAllocationChart() {
        console.log('Rendering Asset Allocation Chart...');
        if (assetAllocationChartInstance) assetAllocationChartInstance.destroy();
        const assetAllocationData = await fetch('/data/chart/asset_allocation').then(res => res.json());
        console.log('Asset Allocation Data:', assetAllocationData);
        const ctx = document.getElementById('asset_allocation_chart').getContext('2d');
        console.log('Asset Allocation Chart Context:', ctx);
        assetAllocationChartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: assetAllocationData.labels,
                datasets: [
                    {
                        data: assetAllocationData.values,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(153, 102, 255, 0.6)',
                            'rgba(255, 159, 64, 0.6)'
                        ],
                        borderColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 206, 86)',
                            'rgb(75, 192, 192)',
                            'rgb(153, 102, 255)',
                            'rgb(255, 159, 64)'
                        ],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Asset Allocation',
                        color: '#ffffff'
                    },
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }

    async function renderTwrChart() {
        console.log('Rendering TWR Chart...');
        if (twrChartInstance) twrChartInstance.destroy();
        const twrData = await fetch('/data/chart/twr_vs_spy').then(res => res.json());
        console.log('TWR Data:', twrData);
        const ctx = document.getElementById('twr_chart').getContext('2d');
        console.log('TWR Chart Context:', ctx);
        twrChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: twrData.dates,
                datasets: [
                    {
                        label: 'Portfolio TWR',
                        data: twrData.portfolio_twr,
                        borderColor: 'rgb(0, 123, 255)',
                        tension: 0.1,
                        fill: false
                    },
                    {
                        label: 'SPY TWR',
                        data: twrData.spy_twr,
                        borderColor: 'rgb(220, 53, 69)',
                        tension: 0.1,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Time-Weighted Return (TWR) vs. SPY',
                        color: '#ffffff'
                    },
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    async function renderCumulativeReturnChart() {
        console.log('Rendering Cumulative Return Chart...');
        if (cumulativeReturnChartInstance) cumulativeReturnChartInstance.destroy();
        const cumulativeReturnData = await fetch('/data/chart/cumulative_cash_flow_adjusted_return').then(res => res.json());
        console.log('Cumulative Return Data:', cumulativeReturnData);
        const ctx = document.getElementById('cumulative_return_chart').getContext('2d');
        console.log('Cumulative Return Chart Context:', ctx);
        cumulativeReturnChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: cumulativeReturnData.dates,
                datasets: [
                    {
                        label: 'Cumulative Cash Flow Adjusted Return',
                        data: cumulativeReturnData.cumulative_return,
                        borderColor: 'rgb(23, 162, 184)',
                        tension: 0.1,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Cumulative Cash Flow Adjusted Return Over Time',
                        color: '#ffffff'
                    },
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#ffffff'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    }

    // Function to initialize DataTables
    function initializeDataTable(tableId, data, columns) {
        // Destroy existing DataTable instance if it exists
        if ($.fn.DataTable.isDataTable(`#${tableId}`)) {
            $(`#${tableId}`).DataTable().destroy();
            $(`#${tableId}`).empty(); // Clear table content
        }

        $(`#${tableId}`).DataTable({
            data: data,
            columns: columns,
            responsive: true,
            paging: true,
            searching: true,
            info: true,
            // Add any other DataTables options you need
        });
    }

    // Function to handle chart tab clicks
    function openChartTab(evt, tabId) {
        console.log(`openChartTab called for tabId: ${tabId}`);
        // Hide all chart content
        chartContents.forEach(tabContent => {
            tabContent.classList.remove('active');
            tabContent.classList.add('hidden'); // Ensure it's hidden
        });

        // Deactivate all tab buttons
        chartTabs.forEach(tabButton => {
            tabButton.classList.remove('active');
        });

        // Show the current tab content and activate its button
        const targetTabContent = document.getElementById(tabId);
        if (targetTabContent) {
            targetTabContent.classList.add('active');
            targetTabContent.classList.remove('hidden'); // Ensure it's visible
        }
        if (evt && evt.currentTarget) {
            evt.currentTarget.classList.add('active');
        }

        // Render the specific chart for the active tab
        switch(tabId) {
            case 'portfolio-value-chart-tab':
                renderPortfolioValueChart();
                break;
            case 'daily-pnl-chart-tab':
                renderDailyPnlChart();
                break;
            case 'asset-allocation-chart-tab':
                renderAssetAllocationChart();
                break;
            case 'twr-chart-tab':
                renderTwrChart();
                break;
            case 'cumulative-return-chart-tab':
                renderCumulativeReturnChart();
                break;
            default:
                console.warn('Unknown tabId:', tabId);
        }
    }

    function loadChartsSection() {
        console.log('loadChartsSection called.');
        showSection('charts-section');
        setActiveLink('nav-charts');
        // Automatically open the first chart tab and render its chart
        const firstTabButton = document.querySelector('.chart-tab-button');
        if (firstTabButton) {
            // Directly call openChartTab to avoid unexpected event cascades
            openChartTab({ currentTarget: firstTabButton }, firstTabButton.dataset.tabId);
        } else {
            console.error('First tab button not found!');
        }
    }

    async function loadPortfolioValuesSection() {
        const portfolioValueData = await fetch('/data/portfolio_value').then(response => response.json());
        if (portfolioValueData.length > 0) {
            const columns = Object.keys(portfolioValueData[0]).map(key => ({ title: key, data: key }));
            initializeDataTable('portfolio_value_table', portfolioValueData, columns);
        } else {
            document.getElementById('portfolio_value_table').innerHTML = '<p>No data available.</p>';
        }
        
        const mddData = await fetch('/data/metrics/maximum_drawdown').then(response => response.json());
        const advancedMetricsData = await fetch('/data/metrics/advanced').then(response => response.json());

        const metricsDisplayDiv = document.getElementById('metrics-display');
        metricsDisplayDiv.innerHTML = `
            <p><strong>Maximum Drawdown:</strong> ${mddData.maximum_drawdown}%</p>
            <p><strong>Sharpe Ratio:</strong> ${advancedMetricsData.sharpe_ratio}</p>
            <p><strong>Sortino Ratio:</strong> ${advancedMetricsData.sortino_ratio}</p>
            <p><strong>Beta:</strong> ${advancedMetricsData.beta}</p>
            <p><strong>Alpha (Annualized):</strong> ${advancedMetricsData.alpha}</p>
        `;

        showSection('portfolio-values-section');
        setActiveLink('nav-portfolio-values');
    }

    async function loadOpenPositionsSection() {
        const openPositionsData = await fetch('/data/open_positions').then(response => response.json());
        if (openPositionsData.length > 0) {
            const columns = Object.keys(openPositionsData[0]).map(key => ({ title: key, data: key }));
            initializeDataTable('open_positions_table', openPositionsData, columns);
        } else {
            document.getElementById('open_positions_table').innerHTML = '<p>No data available.</p>';
        }
        showSection('open-positions-section');
        setActiveLink('nav-open-positions');
    }

    async function loadClosedPositionsSection() {
        const closedPositionsData = await fetch('/data/closed_positions').then(response => response.json());
        if (closedPositionsData.length > 0) {
            const columns = Object.keys(closedPositionsData[0]).map(key => ({ title: key, data: key }));
            initializeDataTable('closed_positions_table', closedPositionsData, columns);
        } else {
            document.getElementById('closed_positions_table').innerHTML = '<p>No data available.</p>';
        }
        showSection('closed-positions-section');
        setActiveLink('nav-closed-positions');
    }

    function loadAddTransactionSection() {
        showSection('add-transaction-section');
        setActiveLink('nav-add-transaction');
    }

    function loadWelcomeSection() {
        showSection('welcome-section');
        setActiveLink('nav-welcome');
    }

    // Event Listeners for Navigation
    document.getElementById('nav-welcome').addEventListener('click', loadWelcomeSection);
    document.getElementById('nav-charts').addEventListener('click', loadChartsSection);
    document.getElementById('nav-portfolio-values').addEventListener('click', loadPortfolioValuesSection);
    document.getElementById('nav-open-positions').addEventListener('click', loadOpenPositionsSection);
    document.getElementById('nav-closed-positions').addEventListener('click', loadClosedPositionsSection);
    document.getElementById('nav-add-transaction').addEventListener('click', loadAddTransactionSection);

    // Attach event listeners to chart tab buttons
    chartTabs.forEach(button => {
        button.addEventListener('click', function(event) {
            openChartTab(event, button.dataset.tabId);
        });
    });

    // Handle form submission
    transactionForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(transactionForm);
        const url = '/transactions';

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            messageParagraph.textContent = data.message;
            if (data.message.includes('successfully')) {
                transactionForm.reset();
                // After adding a transaction, refresh all data and go to charts section
                // Note: Charts are now rendered individually on tab click
                loadPortfolioValuesSection();
                loadOpenPositionsSection();
                loadClosedPositionsSection();
                loadChartsSection(); // Go back to charts after update
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageParagraph.textContent = 'An error occurred while adding the transaction.';
        });
    });

    // Initial load: show welcome section
    loadWelcomeSection();
});