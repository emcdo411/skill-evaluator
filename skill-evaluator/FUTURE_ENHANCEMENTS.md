# Future Enhancements

**Last Updated**: 2025-11-06
**Current Version**: 1.2.1

This document tracks proposed enhancements for future versions of skill-evaluator.

---

## Community Trust Score (v2.0)

**Status**: Design Phase - Planned for v2.0
**Target Version**: 2.0.0
**Priority**: Medium
**Complexity**: High

### Concept

Add a 5th evaluation dimension: **Community Trust** that incorporates social signals to complement security analysis.

### Rationale

**Wisdom of crowds approach**: Popular, well-maintained skills with positive community signals provide additional confidence beyond static analysis.

**Use Cases**:
- New skills with no history: Lower trust score (appropriate caution)
- Established skills from known authors: Higher trust score (deserved confidence)
- Compromised popular packages: Security analysis catches malicious code, trust score doesn't override

### Proposed Metrics

#### GitHub Signals (if hosted on GitHub)
- **Stars**: Popularity/usefulness indicator
- **Forks**: Community engagement
- **Contributors**: Distribution of maintenance
- **Last commit date**: Active maintenance
- **Issues/PRs**: Community involvement
- **Release frequency**: Regular updates

#### Author Reputation
- **Number of published skills**: Experience
- **Average score of other skills**: Track record
- **GitHub profile age**: Established presence

#### Download/Usage Metrics
- **Installation count**: If available from skill registry
- **Community ratings**: If review system exists

### Scoring Approach

**Community Trust Score: 0-100**

Breakdown (25 points each):
1. **Popularity** (25 pts) - Stars, downloads, installations
2. **Maintenance** (25 pts) - Recent commits, release frequency, issue response
3. **Community Engagement** (25 pts) - Contributors, forks, PRs, discussions
4. **Author Reputation** (25 pts) - Profile age, other skills, community standing

### Weighting in Overall Score

**Current weights**:
- Security: 35%
- Quality: 25%
- Utility: 20%
- Compliance: 20%

**Proposed weights with Community Trust**:
- Security: 35% (unchanged - security remains paramount)
- Quality: 20% (reduced from 25%)
- Utility: 15% (reduced from 20%)
- Compliance: 15% (reduced from 20%)
- Community Trust: 15% (new)

**Rationale**: Security remains most important. Community Trust provides additional signal but doesn't override technical analysis.

### Implementation Challenges

#### Data Availability
- ❌ **No central skill registry** - Skills distributed via GitHub, zip files, local directories
- ⚠️ **Git metadata may not exist** - Skills could be downloaded zips without git history
- ⚠️ **Private repositories** - Can't access GitHub API for private repos
- ⚠️ **Non-GitHub skills** - GitLab, Bitbucket, private servers

#### API Limitations
- Rate limiting (GitHub: 60 requests/hour unauthenticated, 5000/hour authenticated)
- Requires authentication for higher limits
- Network dependency (evaluation requires internet)

#### Gaming/Manipulation
- ⚠️ **Stars can be bought** - Fake GitHub stars are purchasable
- ⚠️ **Bots can inflate downloads** - Automated downloads/installations
- ⚠️ **Popularity ≠ security** - Many popular packages have been compromised
- ⚠️ **New ≠ bad** - Legitimate new skills unfairly penalized

#### Edge Cases
- Skill has no repository URL in metadata
- Repository is archived/deleted
- Forked skills vs original
- Multiple versions/branches

### Proposed Implementation

#### Phase 1: Metadata Collection
```python
class CommunityTrustAnalyzer:
    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.repo_url = self._extract_repo_url()

    def _extract_repo_url(self) -> Optional[str]:
        """Extract repository URL from:
        1. SKILL.md frontmatter (repository: field)
        2. .git/config
        3. package.json (if exists)
        """
        pass

    def analyze(self) -> Dict[str, Any]:
        """
        Analyze community trust signals.
        Returns score 0-100 or None if insufficient data.
        """
        if not self.repo_url:
            return {'score': None, 'reason': 'No repository URL found'}

        # Fetch GitHub data
        github_data = self._fetch_github_data()

        # Calculate scores
        popularity = self._score_popularity(github_data)
        maintenance = self._score_maintenance(github_data)
        engagement = self._score_engagement(github_data)
        reputation = self._score_author_reputation(github_data)

        return {
            'score': (popularity + maintenance + engagement + reputation) / 4,
            'breakdown': {...},
            'data_source': self.repo_url
        }
```

#### Phase 2: GitHub API Integration
```python
import requests
from datetime import datetime, timedelta

def _fetch_github_data(self, repo_url: str) -> Optional[Dict]:
    """Fetch repository data from GitHub API."""
    try:
        # Parse owner/repo from URL
        owner, repo = self._parse_github_url(repo_url)

        # Fetch with authentication if available
        headers = {}
        if github_token := os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = f'token {github_token}'

        # Repository metadata
        repo_data = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}',
            headers=headers
        ).json()

        # Recent commits
        commits = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/commits',
            headers=headers,
            params={'per_page': 10}
        ).json()

        return {
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'watchers': repo_data.get('watchers_count', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'created_at': repo_data.get('created_at'),
            'updated_at': repo_data.get('updated_at'),
            'pushed_at': repo_data.get('pushed_at'),
            'recent_commits': commits,
            'contributors_count': len(self._fetch_contributors(owner, repo)),
            'author': repo_data.get('owner', {})
        }
    except Exception as e:
        return None
```

#### Phase 3: Report Integration

Add to report template:
```markdown
### 5. Community Trust Analysis

**Score:** {community_trust_score}/100

**Data Source:** {repo_url}

#### Breakdown
- **Popularity:** {popularity_score}/25 ({stars} stars, {downloads} downloads)
- **Maintenance:** {maintenance_score}/25 (Last updated: {last_update})
- **Engagement:** {engagement_score}/25 ({contributors} contributors, {forks} forks)
- **Author Reputation:** {reputation_score}/25 ({author_skills} published skills)

#### Trust Signals

{trust_signals_list}

#### Limitations

⚠️ **Community signals supplement, but don't replace, security analysis.**
- Popular skills can still contain vulnerabilities
- New skills may be legitimate despite low scores
- Metrics can be manipulated
- Always perform manual review
```

### Caveats and Warnings

#### Must Include in Reports

**If Community Trust is unavailable:**
```
Community Trust score not available:
- No repository URL found in skill metadata
- Repository is private or inaccessible
- Network unavailable or API rate limited

This does NOT indicate the skill is unsafe. Perform manual review.
```

**If score is low:**
```
Low Community Trust score does not necessarily indicate security issues.
- New skills naturally have lower scores
- Private/internal skills may not have public metrics
- Review Security, Quality, and Compliance scores for actual safety
```

**In all reports:**
```
⚠️ Community Trust is based on social signals which can be manipulated.
Always prioritize Security analysis and manual code review.
```

### Alternative: External Registry Integration

If a Claude Skills Registry is established (similar to npm, PyPI):
- Official download counts
- Verified publisher system
- Community ratings/reviews
- Security advisories
- Deprecation notices

This would be more reliable than GitHub stars.

### Recommendation

**Implement in phases**:

1. ✅ **Phase 0 (Current)**: Solid security/quality/compliance analysis
2. 📋 **Phase 1**: Add optional repository URL field to SKILL.md frontmatter
3. 📋 **Phase 2**: Implement GitHub data fetching (optional, with clear fallback)
4. 📋 **Phase 3**: Add Community Trust scoring (clearly marked as supplementary)
5. 📋 **Phase 4**: Integrate with official registry if/when available

**Design principles**:
- Community Trust is **supplementary**, not primary
- **Graceful degradation**: Works without internet/GitHub access
- **Clear disclaimers**: Users understand limitations
- **Security remains paramount**: Trust score doesn't override security findings
- **Fair to new skills**: Documentation explains why scores may be low

### Open Questions

1. Should we penalize skills with *no* repository at all?
2. How much weight for author reputation vs skill reputation?
3. Should we have minimum data thresholds (e.g., must have >3 stars to score)?
4. How to handle forked/modified skills?
5. Should private/enterprise skills be exempt from this scoring?

---

**Discussion needed before implementation.**
