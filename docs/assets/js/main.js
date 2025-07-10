// MCP data structure
const mcpData = {
  "adios": {
    name: "Adios",
    category: "Data Processing",
    description: "Advanced I/O system for scientific data reading from multiple file formats",
    icon: "📊",
    actions: ["read_data", "list_files", "get_metadata"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "arxiv": {
    name: "ArXiv",
    category: "Data Processing", 
    description: "Fetch and search research papers from ArXiv repository",
    icon: "📄",
    actions: ["search_papers", "fetch_paper", "get_metadata"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "hdf5": {
    name: "HDF5",
    category: "Data Processing",
    description: "List and analyze HDF5 files for hierarchical data structures",
    icon: "🗂️",
    actions: ["list_files", "get_structure", "read_dataset"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "pandas": {
    name: "Pandas",
    category: "Data Processing",
    description: "Load, filter, and manipulate CSV data using pandas",
    icon: "🐼",
    actions: ["load_csv", "filter_data", "get_info", "describe"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "parquet": {
    name: "Parquet",
    category: "Data Processing",
    description: "Read and analyze Parquet file columns and metadata",
    icon: "📋",
    actions: ["read_columns", "get_schema", "list_files"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "plot": {
    name: "Plot",
    category: "Analysis & Visualization",
    description: "Create visualizations and plots from CSV data",
    icon: "📈",
    actions: ["create_plot", "scatter_plot", "histogram", "save_plot"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "darshan": {
    name: "Darshan",
    category: "Analysis & Visualization",
    description: "I/O performance analysis and monitoring tool",
    icon: "⚡",
    actions: ["analyze_io", "get_stats", "generate_report"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "slurm": {
    name: "Slurm",
    category: "System Management",
    description: "Job submission and management simulation for HPC environments",
    icon: "🖥️",
    actions: ["submit_job", "check_status", "cancel_job", "get_queue"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "lmod": {
    name: "Lmod",
    category: "System Management",
    description: "Environment module management for scientific computing",
    icon: "📦",
    actions: ["list_modules", "load_module", "unload_module", "get_info"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "node_hardware": {
    name: "Node Hardware",
    category: "System Management",
    description: "CPU core and hardware information reporting",
    icon: "💻",
    actions: ["get_cores", "get_memory", "get_info"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "compression": {
    name: "Compression",
    category: "Utilities",
    description: "File compression and decompression simulation",
    icon: "🗜️",
    actions: ["compress_file", "decompress_file", "get_ratio"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "parallel_sort": {
    name: "Parallel Sort",
    category: "Utilities",
    description: "Large file sorting with parallel processing capabilities",
    icon: "🔄",
    actions: ["sort_file", "merge_files", "get_status"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  },
  "jarvis": {
    name: "Jarvis",
    category: "Utilities",
    description: "Data pipeline management and workflow automation",
    icon: "🤖",
    actions: ["create_pipeline", "run_workflow", "get_status", "manage_data"],
    stats: { version: "1.0.0", updated: "2024-01-15" }
  }
};

// Categories
const categories = {
  "All": { count: Object.keys(mcpData).length, color: "#6b7280" },
  "Data Processing": { count: 5, color: "#3b82f6" },
  "Analysis & Visualization": { count: 2, color: "#10b981" },
  "System Management": { count: 3, color: "#f59e0b" },
  "Utilities": { count: 3, color: "#ef4444" }
};

// DOM elements
let searchInput, mcpGrid, categoryLinks, mcpCards;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeElements();
  renderCategories();
  renderMCPs();
  setupEventListeners();
});

function initializeElements() {
  searchInput = document.getElementById('search-input');
  mcpGrid = document.getElementById('mcp-grid');
  categoryLinks = document.querySelectorAll('.category-link');
  
  // Create MCP grid if it doesn't exist
  if (!mcpGrid) {
    mcpGrid = document.createElement('div');
    mcpGrid.id = 'mcp-grid';
    mcpGrid.className = 'mcp-grid';
    document.querySelector('.content')?.appendChild(mcpGrid);
  }
}

function renderCategories() {
  const categoryList = document.getElementById('category-list');
  if (!categoryList) return;
  
  categoryList.innerHTML = '';
  
  Object.entries(categories).forEach(([category, data]) => {
    const li = document.createElement('li');
    li.className = 'category-item';
    
    const link = document.createElement('a');
    link.href = '#';
    link.className = 'category-link';
    link.dataset.category = category;
    if (category === 'All') link.classList.add('active');
    
    link.innerHTML = `
      ${category}
      <span class="category-count">${data.count}</span>
    `;
    
    li.appendChild(link);
    categoryList.appendChild(li);
  });
}

function renderMCPs(filteredData = mcpData, activeCategory = 'All') {
  if (!mcpGrid) return;
  
  mcpGrid.innerHTML = '';
  
  Object.entries(filteredData).forEach(([key, mcp]) => {
    const card = createMCPCard(key, mcp);
    mcpGrid.appendChild(card);
  });
  
  // Update category counts
  updateCategoryCounts(filteredData);
}

function createMCPCard(key, mcp) {
  const card = document.createElement('a');
  card.href = `mcps/${key}.html`;
  card.className = 'mcp-card';
  card.dataset.category = mcp.category;
  card.dataset.name = mcp.name.toLowerCase();
  
  card.innerHTML = `
    <div class="mcp-header">
      <div class="mcp-icon">${mcp.icon}</div>
      <div>
        <h3 class="mcp-title">${mcp.name}</h3>
        <span class="mcp-category">${mcp.category}</span>
      </div>
    </div>
    <p class="mcp-description">${mcp.description}</p>
    <div class="mcp-stats">
      <div class="mcp-stat">
        <span>📦</span>
        <span>v${mcp.stats.version}</span>
      </div>
      <div class="mcp-stat">
        <span>📅</span>
        <span>${mcp.stats.updated}</span>
      </div>
    </div>
    <div class="mcp-actions">
      ${mcp.actions.map(action => `<span class="action-tag">${action}</span>`).join('')}
    </div>
  `;
  
  return card;
}

function setupEventListeners() {
  // Search functionality
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
  }
  
  // Category filtering
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('category-link')) {
      e.preventDefault();
      handleCategoryFilter(e.target);
    }
  });
  
  // Tab functionality for detail pages
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('tab')) {
      handleTabClick(e.target);
    }
  });
}

function handleSearch() {
  const query = searchInput.value.toLowerCase().trim();
  const activeCategory = document.querySelector('.category-link.active')?.dataset.category || 'All';
  
  let filteredData = mcpData;
  
  // Filter by category
  if (activeCategory !== 'All') {
    filteredData = Object.fromEntries(
      Object.entries(mcpData).filter(([key, mcp]) => mcp.category === activeCategory)
    );
  }
  
  // Filter by search query
  if (query) {
    filteredData = Object.fromEntries(
      Object.entries(filteredData).filter(([key, mcp]) => 
        mcp.name.toLowerCase().includes(query) ||
        mcp.description.toLowerCase().includes(query) ||
        mcp.category.toLowerCase().includes(query) ||
        mcp.actions.some(action => action.toLowerCase().includes(query))
      )
    );
  }
  
  renderMCPs(filteredData, activeCategory);
}

function handleCategoryFilter(link) {
  // Update active category
  document.querySelectorAll('.category-link').forEach(l => l.classList.remove('active'));
  link.classList.add('active');
  
  const category = link.dataset.category;
  let filteredData = mcpData;
  
  // Filter by category
  if (category !== 'All') {
    filteredData = Object.fromEntries(
      Object.entries(mcpData).filter(([key, mcp]) => mcp.category === category)
    );
  }
  
  // Apply current search query
  const query = searchInput?.value.toLowerCase().trim();
  if (query) {
    filteredData = Object.fromEntries(
      Object.entries(filteredData).filter(([key, mcp]) => 
        mcp.name.toLowerCase().includes(query) ||
        mcp.description.toLowerCase().includes(query) ||
        mcp.category.toLowerCase().includes(query) ||
        mcp.actions.some(action => action.toLowerCase().includes(query))
      )
    );
  }
  
  renderMCPs(filteredData, category);
}

function updateCategoryCounts(filteredData) {
  const categoryCounts = {};
  
  Object.values(filteredData).forEach(mcp => {
    categoryCounts[mcp.category] = (categoryCounts[mcp.category] || 0) + 1;
  });
  
  categoryCounts['All'] = Object.keys(filteredData).length;
  
  document.querySelectorAll('.category-link').forEach(link => {
    const category = link.dataset.category;
    const countElement = link.querySelector('.category-count');
    if (countElement) {
      countElement.textContent = categoryCounts[category] || 0;
    }
  });
}

function handleTabClick(tab) {
  const tabContainer = tab.closest('.tabs').parentElement;
  
  // Remove active class from all tabs and content
  tabContainer.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  tabContainer.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  
  // Add active class to clicked tab
  tab.classList.add('active');
  
  // Show corresponding content
  const targetContent = document.getElementById(tab.dataset.tab);
  if (targetContent) {
    targetContent.classList.add('active');
  }
}

// Utility functions
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
}

function generateInstallCommand(mcpName) {
  return `uv pip install "scientific-mcps[${mcpName}]"`;
}

function generateServerCommand(mcpName) {
  return `uv run mcp_${mcpName}`;
}

// Export for use in other files
window.mcpData = mcpData;
window.categories = categories;