# Contractor Prospector Skill

**Purpose:** Find contractors who don't have websites (or only have social media presence), build them a demo site, and email them an offer.

**Target verticals (expandable):**
- Artificial turf installation
- Landscaping
- Pressure washing
- Pool cleaning
- HVAC
- Roofing
- Fencing
- Concrete/paving

---

## WORKFLOW OVERVIEW

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PROSPECT      │ --> │   ENRICH        │ --> │   BUILD SITE    │ --> │   OUTREACH      │
│   (Find leads)  │     │   (Get details) │     │   (GitHub Pages)│     │   (Send email)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## PHASE 1: PROSPECTING

### Search Strategy

Use `mcporter call firecrawl.firecrawl_search` for ALL prospecting.

**Query Templates:**
```
"{service} {city} {state}"
"site:facebook.com {service} {city}"
"site:yelp.com {service} near {city} {state}"
```

**What you're looking for:**
- Businesses with NO website in search results
- Businesses where the only link is facebook.com or instagram.com
- Yelp/Google listings with phone but no website
- Facebook business pages

### Cities to Target
Configure based on your service area. South Florida example:
```
Miami, Fort Lauderdale, Boca Raton, West Palm Beach, Hollywood, 
Pompano Beach, Coral Springs, Plantation, Sunrise, Pembroke Pines
```

### Prospect Data to Capture

For each prospect, collect:
```json
{
  "business_name": "Example Pro Services",
  "phone": "555-000-1234",
  "email": null,
  "city": "Your City",
  "state": "FL",
  "service_type": "artificial turf installation",
  "social_url": "https://facebook.com/examplebusiness",
  "social_bio": "Professional installation. 10+ years experience.",
  "found_via": "facebook search",
  "has_website": false,
  "source_date": "2026-01-01"
}
```

---

## PHASE 2: ENRICHMENT

### Getting Contact Info

**From Facebook pages:**
- Check the "About" section for phone/email
- Look at "Contact" or "Info" tabs
- Note their service description

**From Yelp:**
- Phone is usually listed
- Service area descriptions
- Reviews can show quality/style

**Finding Email (if not listed):**
- Try: info@{businessname}.com
- Look for email in FB "About"
- Sometimes listed in Google Maps listing

---

## PHASE 3: SITE GENERATION

### Template System

Use the HTML template at:
`{skills_dir}/contractor-prospector/templates/contractor-site.html`

**Template Variables:**
- `{{BUSINESS_NAME}}` - Company name
- `{{TAGLINE}}` - From their social bio or generate one
- `{{PHONE}}` - Their phone number
- `{{CITY}}` - Service area city
- `{{STATE}}` - State abbreviation
- `{{SERVICE_TYPE}}` - e.g., "Artificial Turf Installation"
- `{{SERVICE_DESCRIPTION}}` - 2-3 sentences about what they do
- `{{YEAR}}` - Current year for copyright

### Deploying to GitHub Pages

**Step 1: Create the filled HTML**
Read the template, replace all `{{VARIABLES}}` with actual values.

**Step 2: Create repo and push**
```powershell
$slug = "business-name-demo"   # lowercase, hyphens
$tempDir = "$env:TEMP\contractor-deploy-$slug"

New-Item -ItemType Directory -Path $tempDir -Force
Set-Location $tempDir

$html | Out-File -FilePath "index.html" -Encoding utf8

git init
git add .
git commit -m "Initial demo site"
gh repo create $slug --public --source=. --push

# Enable GitHub Pages
gh api "repos/$(gh api user --jq '.login')/$slug/pages" -X POST -f "source[branch]=main" -f "source[path]=/"
```

**Step 3: Get the live URL**
```
https://{your-github-username}.github.io/{slug}/
```

---

## PHASE 4: OUTREACH

### Email Template (Primary)

**Subject:** I built your website - take a look 👀

```
Hey [First Name],

I came across [Business Name] and noticed you don't have a website yet.

So I built you one: [DEMO URL]

It's mobile-friendly, loads fast, and already has your phone number so customers can call directly.

If you want it:
• $299 one-time (yours forever, includes 1 year hosting)
• $49/month managed (I handle updates, hosting, everything)

No pressure. Just wanted to show you what's possible.

Hit reply if interested.

[Your Name]
[Your Business]
```

**Send using:**
```
email_send to:{prospect_email} subject:"I built your website - take a look 👀" body:{filled_template}
```

---

## FULL AUTOMATION LOOP

When told to "prospect" or "run the prospector":

1. **Pick a vertical** (ask if not specified)
2. **Pick a city** (rotate through the list)
3. **Run ONE smart search** (respect rate limits!)
4. **Extract 2-3 prospects** from results
5. **Enrich** each prospect (get phone, bio, etc.)
6. **Build demo site** for each
7. **Send outreach email** (if email available) or log for manual follow-up
8. **Report results** to user

**Pace yourself:** 3-5 prospects per session max. Quality over quantity.

---

## QUICK COMMANDS

- `"Prospect [service type] companies in [city]"` - Full workflow for one city
- `"Build a site for [Business Name]"` - Just build site
- `"Send outreach to [email] for [business]"` - Just send email
- `"Show me today's prospects"` - Review what's been found

---

## SAFETY & LIMITS

- **GitHub:** No hard limits, but don't spam repos.
- **Email:** Don't send more than 20/day to avoid spam flags.
- **Quality:** Better to have 3 great prospects than 30 garbage ones.
