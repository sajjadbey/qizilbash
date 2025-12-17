# API Map

## Base URL
All endpoints are prefixed with the base URL of your Django application.

---

## 1. Dictionary API (`/api/dict/`)

### 1.1 Get All Words
- **Endpoint:** `GET /api/dict/all/`
- **Description:** Retrieve all words in the dictionary
- **Response:** Array of word objects
- **Response Fields:**
  - `id` - Word ID
  - `word` - Azerbaijani word
  - `english_translation` - English translation
  - `persian_translation` - Persian translation
  - `meaning_english` - English meaning/definition
  - `meaning_azerbaijani` - Azerbaijani meaning/definition
  - `word_type` - Type of word (noun, verb, etc.)
  - `created_at` - Creation timestamp

### 1.2 Search Words
- **Endpoint:** `GET /api/dict/search/`
- **Description:** Search for words containing the query text
- **Query Parameters:**
  - `text` (required) - Search query string
- **Example:** `/api/dict/search/?text=salam`
- **Response:** Array of matching word objects

### 1.3 Get Word Detail
- **Endpoint:** `GET /api/dict/<word>/`
- **Description:** Get details of a specific word by its Azerbaijani spelling (case-insensitive)
- **Example:** `/api/dict/salam/`
- **Response:** Single word object

---

## 2. Text Converter API (`/api/convert/`)

### 2.1 Convert Text
- **Endpoint:** `GET /api/convert/`
- **Description:** Convert text between Latin and Arabic scripts
- **Query Parameters:**
  - `text` (required) - Text to convert
  - `source` (required) - Source script (`latin`)
  - `target` (required) - Target script (`arabic`)
- **Example:** `/api/convert/?text=salam&source=latin&target=arabic`
- **Response:**
  ```json
  {
    "result": "سلام"
  }
  ```
- **Note:** Currently only supports Latin → Arabic conversion

---

## 3. Genetics API (`/genetics/`)

### 3.1 Genetic Samples
- **Endpoint:** `GET /genetics/samples/`
- **Description:** Retrieve genetic samples with optional filtering
- **Query Parameters:**
  - `country` - Filter by country name
  - `province` - Filter by province name
  - `city` - Filter by city name
  - `ethnicity` - Filter by ethnicity name
  - `tribe` - Filter by tribe name
  - `clan` - Filter by clan name
- **Filtering Logic:**
  - Location cascade: city > province > country (most specific wins)
  - Hierarchy: clan > tribe
- **Response Fields:**
  - `name` - Sample name
  - `country` - Country name
  - `province` - Province name
  - `city` - City name
  - `ethnicity` - Ethnicity name
  - `tribe` - Tribe name
  - `clan` - Clan name
  - `y_dna` - Y-DNA haplogroup object with `name` and `root_haplogroup`
  - `mt_dna` - Mitochondrial DNA haplogroup object with `name` and `root_haplogroup`
  - `historical_period` - Historical period object with `name`, `start_year`, `end_year`, `display`
  - `description` - Sample description
  - `count` - Number of samples
  - `coordinates` - Location coordinates object with `latitude` and `longitude`

### 3.2 Countries
- **Endpoint:** `GET /genetics/countries/`
- **Description:** List all countries
- **Response Fields:**
  - `name` - Country name

### 3.3 Provinces
- **Endpoint:** `GET /genetics/provinces/`
- **Description:** List provinces with optional country filtering
- **Query Parameters:**
  - `country` - Filter by country name
- **Response Fields:**
  - `name` - Province name
  - `country` - Country name
  - `latitude` - Latitude coordinate (extracted from geometry centroid)
  - `longitude` - Longitude coordinate (extracted from geometry centroid)
  - `geometry` - GeoJSON geometry object (MultiPolygon) representing province boundary
- **GeoJSON Geometry Format:**
  ```json
  {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [longitude, latitude],
          [longitude, latitude],
          ...
        ]
      ]
    ]
  }
  ```
- **Note:** Coordinates are calculated from the province's MultiPolygon geometry centroid. The geometry field contains the full province boundary as GeoJSON.

### 3.4 Cities
- **Endpoint:** `GET /genetics/cities/`
- **Description:** List cities with optional province filtering
- **Query Parameters:**
  - `province` - Filter by province name
- **Response Fields:**
  - `name` - City name
  - `province` - Province name

### 3.5 Ethnicities
- **Endpoint:** `GET /genetics/ethnicities/`
- **Description:** List ethnicities with optional location filtering
- **Query Parameters:**
  - `country` - Filter by country name
  - `province` - Filter by province name
- **Response Fields:**
  - `name` - Ethnicity name

### 3.6 Tribes
- **Endpoint:** `GET /genetics/tribes/`
- **Description:** List tribes with optional ethnicity filtering
- **Query Parameters:**
  - `ethnicity` - Filter by ethnicity name (returns tribes that have this ethnicity)
- **Response Fields:**
  - `name` - Tribe name
  - `ethnicities` - Array of ethnicity names (can be empty array)
  - `historical_note` - Historical/cultural note about the tribe

### 3.7 Clans
- **Endpoint:** `GET /genetics/clans/`
- **Description:** List clans with optional filtering
- **Query Parameters:**
  - `tribe` - Filter by tribe name
  - `ethnicity` - Filter by ethnicity name (if tribe not specified, returns clans whose tribe has this ethnicity)
- **Response Fields:**
  - `name` - Clan name
  - `tribe` - Tribe name
  - `ethnicities` - Array of ethnicity names from the tribe (can be empty array)
  - `common_ancestor` - Name of common ancestor

### 3.8 Haplogroup Count
- **Endpoint:** `GET /genetics/haplogroup/`
- **Description:** Get total count of samples for a haplogroup including all subclades
- **Query Parameters:**
  - `name` (required) - Haplogroup name (e.g., "R")
- **Example:** `/genetics/haplogroup/?name=R`
- **Response Fields:**
  - `haplogroup` - Haplogroup name
  - `total_count` - Total sample count including all subclades
  - `direct_count` - Direct sample count for this haplogroup only
  - `subclade_count` - Number of unique subclades
  - `subclades` - Array of subclade names

### 3.9 Haplogroup List (Hierarchical)
- **Endpoint:** `GET /genetics/haplogroup/all/`
- **Description:** List all haplogroups in hierarchical tree structure
- **Response:** Nested tree structure with:
  - `name` - Haplogroup name
  - `root_haplogroup` - Root haplogroup name (null for root nodes)
  - `children` - Array of child haplogroups (recursive structure)

### 3.10 Haplogroup Heatmap
- **Endpoint:** `GET /genetics/haplogroup/heatmap/`
- **Description:** Get aggregated sample counts by location with GeoJSON geometry for heatmap visualization
- **Query Parameters:**
  - `haplogroup` - Filter by Y-DNA haplogroup (includes subclades)
  - `country` - Filter by country
  - `ethnicity` - Filter by ethnicity
- **Examples:**
  - `/genetics/haplogroup/heatmap/` - All samples
  - `/genetics/haplogroup/heatmap/?haplogroup=R` - R haplogroup and subclades
  - `/genetics/haplogroup/heatmap/?country=Iran` - Samples from Iran
- **Response:** Array of location objects with:
  - `province` - Province name
  - `country` - Country name
  - `latitude` - Latitude coordinate (extracted from geometry centroid)
  - `longitude` - Longitude coordinate (extracted from geometry centroid)
  - `geometry` - GeoJSON geometry object (MultiPolygon)
  - `sample_count` - Aggregated sample count
  - `haplogroup` - Haplogroup filter (if applied)
- **GeoJSON Geometry Format:**
  ```json
  {
    "type": "MultiPolygon",
    "coordinates": [
      [
        [
          [longitude, latitude],
          [longitude, latitude],
          ...
        ]
      ]
    ]
  }
  ```
- **Note:** Results are sorted by sample count (descending). Coordinates are calculated from province geometry centroids. The geometry field contains the full province boundary as GeoJSON.

### 3.11 Blog Posts List
- **Endpoint:** `GET /genetics/blog/`
- **Description:** List all published blog posts
- **Query Parameters:**
  - `tag` - Filter by tag (partial match)
  - `search` - Search in title, content, and excerpt
- **Examples:**
  - `/genetics/blog/` - All published posts
  - `/genetics/blog/?tag=genetics` - Posts tagged with "genetics"
  - `/genetics/blog/?search=haplogroup` - Posts containing "haplogroup"
- **Response:** Array of blog post objects with:
  - `id` - Blog post ID
  - `title` - Post title
  - `slug` - URL-friendly slug
  - `content` - Full post content in Markdown format
  - `excerpt` - Short summary
  - `author` - Author name
  - `featured_image` - URL to featured image (can be null)
  - `meta_description` - SEO meta description
  - `tags` - Comma-separated tags string
  - `tags_list` - Array of individual tags
  - `created_at` - Creation timestamp
  - `updated_at` - Last update timestamp
  - `published_at` - Publication timestamp
  - `view_count` - Number of views
- **Note:** Only published posts are returned. Results are ordered by publication date (newest first).

### 3.12 Blog Post Detail
- **Endpoint:** `GET /genetics/blog/<slug>/`
- **Description:** Get a single blog post by slug and increment view count
- **Example:** `/genetics/blog/introduction-to-y-dna/`
- **Response:** Single blog post object (same fields as list endpoint)
- **Note:** Each request increments the `view_count` by 1. Only published posts are accessible.

### 3.13 Blog Management
- **Description:** Blog posts can only be created, updated, and deleted through the Django Admin Panel
- **Admin URL:** `/admin/genetics/blogpost/`
- **Features:**
  - Create new posts with title, slug, content, excerpt, tags, etc.
  - Set post status (draft, published, archived)
  - Auto-generate slugs from titles
  - Set publication dates
  - Upload featured images
  - Add SEO meta descriptions
- **Note:** Public API endpoints are read-only. All write operations require admin access.

---

## 4. Admin Panel
- **Endpoint:** `/admin/`
- **Description:** Django admin interface for data management

---

## Response Formats

### Success Response
All successful API calls return JSON data with appropriate HTTP status codes (200, 201, etc.)

### Error Response
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## Notes

1. **Pagination:** Most list endpoints have pagination disabled (`pagination_class = None`)
2. **Filtering:** Many endpoints support hierarchical filtering (e.g., city > province > country)
3. **Case Sensitivity:** Word searches are case-insensitive
4. **Coordinates:** Location coordinates are extracted from province geometry centroids (MultiPolygon fields)
5. **Haplogroup Hierarchy:** Haplogroup queries automatically include all descendant subclades
6. **URL Encoding:** Text parameters should be URL-encoded (especially for special characters like 'ə')