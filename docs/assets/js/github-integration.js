// GitHub API integration for dynamic stats
class GitHubIntegration {
  constructor() {
    this.baseUrl = 'https://api.github.com';
    this.repoOwner = 'iowarp';
    this.repoName = 'scientific-mcps';
    this.cache = new Map();
    this.cacheExpiry = 15 * 60 * 1000; // 15 minutes
  }

  async fetchRepoStats() {
    const cacheKey = 'repo-stats';
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }

    try {
      const response = await fetch(`${this.baseUrl}/repos/${this.repoOwner}/${this.repoName}`);
      if (!response.ok) throw new Error('Failed to fetch repo stats');
      
      const data = await response.json();
      const stats = {
        stars: data.stargazers_count,
        forks: data.forks_count,
        issues: data.open_issues_count,
        lastUpdated: new Date(data.updated_at).toLocaleDateString(),
        language: data.language,
        license: data.license?.name || 'Not specified',
        description: data.description
      };

      this.cache.set(cacheKey, {
        data: stats,
        timestamp: Date.now()
      });

      return stats;
    } catch (error) {
      console.warn('Failed to fetch GitHub stats:', error);
      return null;
    }
  }

  async fetchReleases() {
    const cacheKey = 'releases';
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }

    try {
      const response = await fetch(`${this.baseUrl}/repos/${this.repoOwner}/${this.repoName}/releases`);
      if (!response.ok) throw new Error('Failed to fetch releases');
      
      const data = await response.json();
      const releases = data.slice(0, 5).map(release => ({
        name: release.name,
        tagName: release.tag_name,
        publishedAt: new Date(release.published_at).toLocaleDateString(),
        body: release.body,
        htmlUrl: release.html_url
      }));

      this.cache.set(cacheKey, {
        data: releases,
        timestamp: Date.now()
      });

      return releases;
    } catch (error) {
      console.warn('Failed to fetch releases:', error);
      return [];
    }
  }

  async fetchContributors() {
    const cacheKey = 'contributors';
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }

    try {
      const response = await fetch(`${this.baseUrl}/repos/${this.repoOwner}/${this.repoName}/contributors`);
      if (!response.ok) throw new Error('Failed to fetch contributors');
      
      const data = await response.json();
      const contributors = data.slice(0, 10).map(contributor => ({
        login: contributor.login,
        avatarUrl: contributor.avatar_url,
        contributions: contributor.contributions,
        htmlUrl: contributor.html_url
      }));

      this.cache.set(cacheKey, {
        data: contributors,
        timestamp: Date.now()
      });

      return contributors;
    } catch (error) {
      console.warn('Failed to fetch contributors:', error);
      return [];
    }
  }

  async updatePageWithStats() {
    const stats = await this.fetchRepoStats();
    if (!stats) return;

    // Update homepage stats if elements exist
    const starsElement = document.querySelector('[data-stat="stars"]');
    const forksElement = document.querySelector('[data-stat="forks"]');
    const issuesElement = document.querySelector('[data-stat="issues"]');
    const lastUpdatedElement = document.querySelector('[data-stat="last-updated"]');

    if (starsElement) starsElement.textContent = stats.stars;
    if (forksElement) forksElement.textContent = stats.forks;
    if (issuesElement) issuesElement.textContent = stats.issues;
    if (lastUpdatedElement) lastUpdatedElement.textContent = stats.lastUpdated;

    // Update detail pages if they exist
    const detailStatsElements = document.querySelectorAll('.detail-stats .stat-value');
    detailStatsElements.forEach(element => {
      const label = element.nextElementSibling?.textContent.toLowerCase();
      if (label === 'updated' || label === 'last updated') {
        element.textContent = stats.lastUpdated;
      }
    });
  }

  async addStatsToHomepage() {
    const stats = await this.fetchRepoStats();
    if (!stats) return;

    // Add stats section to homepage
    const heroSection = document.querySelector('.hero');
    if (heroSection && !document.querySelector('.repo-stats')) {
      const statsHtml = `
        <div class="repo-stats" style="margin-top: 2rem; display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;">
          <div class="repo-stat">
            <span class="stat-icon">⭐</span>
            <span class="stat-value" data-stat="stars">${stats.stars}</span>
            <span class="stat-label">Stars</span>
          </div>
          <div class="repo-stat">
            <span class="stat-icon">🍴</span>
            <span class="stat-value" data-stat="forks">${stats.forks}</span>
            <span class="stat-label">Forks</span>
          </div>
          <div class="repo-stat">
            <span class="stat-icon">🐛</span>
            <span class="stat-value" data-stat="issues">${stats.issues}</span>
            <span class="stat-label">Issues</span>
          </div>
        </div>
      `;
      
      heroSection.insertAdjacentHTML('beforeend', statsHtml);
      
      // Add CSS for repo stats
      const style = document.createElement('style');
      style.textContent = `
        .repo-stats {
          margin-top: 2rem;
          display: flex;
          gap: 2rem;
          justify-content: center;
          flex-wrap: wrap;
        }
        
        .repo-stat {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.25rem;
          color: rgba(255, 255, 255, 0.9);
        }
        
        .repo-stat .stat-icon {
          font-size: 1.5rem;
        }
        
        .repo-stat .stat-value {
          font-size: 1.25rem;
          font-weight: 700;
          color: white;
        }
        
        .repo-stat .stat-label {
          font-size: 0.875rem;
          color: rgba(255, 255, 255, 0.7);
          text-transform: uppercase;
          letter-spacing: 0.025em;
        }
        
        @media (max-width: 480px) {
          .repo-stats {
            gap: 1rem;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }
}

// Initialize GitHub integration
const githubIntegration = new GitHubIntegration();

// Update stats when page loads
document.addEventListener('DOMContentLoaded', function() {
  githubIntegration.updatePageWithStats();
  githubIntegration.addStatsToHomepage();
});

// Refresh stats periodically
setInterval(() => {
  githubIntegration.updatePageWithStats();
}, 5 * 60 * 1000); // Every 5 minutes

// Export for use in other files
window.githubIntegration = githubIntegration;