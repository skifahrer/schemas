# schemas

The file formats of Riki Maps, the skifahrer/maptiles pipeline and skifahrer/traffic-signs, as
JSON Schema 2020-12. This repository is their only home: the app and the pipelines pull the
schemas from here when they need them and carry no copy.

Three kinds of file, each holding one or more of what it is for:

| Format | What it holds | Schema |
|---|---|---|
| [`.mapson`](#mapson) | one or more maps as JSON: settings, layers, their networks and styles; no downloaded data | [`mapson.schema.json`](schema/v1/mapson.schema.json) |
| [`.servson`](#servson) | one or more servers as JSON, with their subservers, everything they published and, when chosen, their credentials | [`servson.schema.json`](schema/v1/servson.schema.json) |
| [`.mapspack`](#mapspack) | maps with their downloaded data: a mapson plus tiles and feature files, as a folder | [`mapspack.schema.json`](schema/v1/mapspack.schema.json) (its `package.json`) |

A mapspack travels as one file, in either of two archives:

| Archive | What it is | Schema |
|---|---|---|
| [`.mapszip`](#mapszip) | a mapspack in Riki Maps' own container, readable without unpacking | [`mapszip.schema.json`](schema/v1/mapszip.schema.json) (its manifest) |
| [`.mapsaar`](#mapsaar) | a mapspack as an Apple Archive, which any Mac unpacks | none of its own: it is the mapspack's |

And one the pipeline publishes:

| | | |
|---|---|---|
| [`maps.json`](#mapsjson) | the region catalog skifahrer/maptiles publishes | [`maps.schema.json`](schema/v1/maps.schema.json) |

And the files of [skifahrer/traffic-signs](#traffic-signs):

| File | What it holds | Schema |
|---|---|---|
| [`<sign>-<country>.json`](#one-countrys-sign) | one country's version of a sign: its code, image and source | [`sign.schema.json`](schema/v1/sign.schema.json) |
| [`<sign>.json`](#a-signs-names) | a sign's names, one per language | [`sign-names.schema.json`](schema/v1/sign-names.schema.json) |
| [`data.json`](#the-viewers-datajson) | everything the traffic signs viewer shows | [`signs-data.schema.json`](schema/v1/signs-data.schema.json) |

Every schema is published at
`https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/<name>.schema.json`.

## mapson

Maps + JSON. One map, or several, as JSON: each map's settings, its layers and how each is
fetched (addresses, request setups, proxies, keys when chosen) and drawn, and its styles. It
holds no downloaded data; a [mapspack](#mapspack) does. Riki Maps reads and writes it as
`.mapson`, and anyone else can too.

| | |
|---|---|
| Schema | [`schema/v1/mapson.schema.json`](schema/v1/mapson.schema.json) (JSON Schema 2020-12) |
| Schema URL | `https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/mapson.schema.json` |
| Examples | [`examples/minimal.mapson`](examples/minimal.mapson), [`examples/full.mapson`](examples/full.mapson), [`examples/two-maps.mapson`](examples/two-maps.mapson) |
| Media | UTF-8 JSON, extension `.mapson` (`.rikimap` is the legacy name), UTI `com.rikimaps.mapson` |

### Shape

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/mapson.schema.json",
  "_schemaVersion": 1,
  "id": "0834FFB7-67BA-4327-87F2-E18AEE11B2FC",
  "name": "OpenStreetMap",
  "isBuiltIn": false, "drawsRegions": false, "isOnlineOnly": false,
  "stack": [ /* layers, index 0 drawn first */ ],
  "styles": [ /* may be empty */ ]
}
```

Every object in the schema lists its **required** keys in `required`. Every other key it
names is **optional**. Here are the required ones:

| Object | Required keys |
|---|---|
| map (root, or each of `maps[]`) | `id` `name` `stack` `styles` `isBuiltIn` `drawsRegions` `isOnlineOnly` |
| collection (root with `maps`) | `_schemaVersion` (2) `maps` |
| layer (`stack[]`) | `id` `name` `symbol` `role` `opacity` `source` `isEnabled` |
| layer `source` | exactly one of `region` `url` `files` `apple` |
| `source.url` | `template` `maxZoom` `format` `attribution` |
| style (`styles[]`) | `id` `name` `symbol` `origin` `notes` `adjustments` |
| style `origin` | exactly one of `builtIn` `document` `arrangement` (`{}`) |
| style `adjustments` | `lineWidthScale` `labelSizeScale` |
| credit (`credits[]`) | `holder` |

The schema lists every nested object: Esri services, API readings, renderers,
arrangements and the rest.

### Names and a note in other languages

Optional. A map may carry a `note` for its readers, and the map and each style may carry their
name, and the map its note, in other languages:

```jsonc
{ "name": "Tatry v zime", "nameTranslations": { "en": "Tatras in winter", "de": "Tatra im Winter" },
  "note": "Stiahnite si najprv Prešovský kraj.", "noteTranslations": { "en": "Download Prešov first." } }
```

Keys are language tags as Apple's `.lproj` folders name them (`de`, `pt-BR`, `zh-Hans`). A reader
shows the text for the language it runs in (`pt-BR` also takes `pt`), else `name` or `note`. The
texts travel with the map: a file, iCloud, a shared map.

### Regions a layer needs

A `region` layer may name the [maps.json](#mapsjson) regions it needs, by [id](#region-ids):

```jsonc
{ "source": { "region": { "overlay": "cartography" } },
  "requiredRegions": ["slovakia-presovsky", "slovakia-zilinsky"] }
```

A reader that opens the map offers to download those it doesn't hold. The list travels with the
map wherever it goes: a file, iCloud, a shared map.

### Where a map works

`coverage` says where the map has its features and tiles: the whole world, whole countries
(ISO 3166-1 alpha-2, upper case), parts of countries (maps.json [ids](#region-ids)), or
countries and regions together. Riki Maps asks for it when a map is sent to the gallery, whose
chips filter by it.

```jsonc
{ "coverage": { "world": true } }
{ "coverage": { "countries": ["SK", "PL"], "regions": ["austria-burgenland"] } }
```

With `world` true, `countries` and `regions` are not read. Absent says nothing about it.

### Keys left out, and how to get them

A map exported without its keys (the gallery's copies always are) leaves out `rikiHeaders`
and the query keys in its addresses. It says what it left out in `access.missingKeys`, and its
author can say how readers get their own keys in `access.keysNote` and link the map's manual
in `access.manualURL`:

```jsonc
{ "access": {
    "keysNote": "Sign up at https://tiles.example/signup and copy the key from your account.",
    "keysNoteTranslations": { "sk": "Zaregistrujte sa na https://tiles.example/signup." },
    "manualURL": "https://tiles.example/docs/ortofoto",
    "missingKeys": [
      { "host": "tiles.example", "name": "apikey", "place": "query" },
      { "host": "tiles.example", "name": "X-Api-Token", "place": "header" } ] } }
```

A reader asks for each missing key when the map is added, or later from the map's settings: a
`query` key goes back into every address of that host, a `header` key is sent with each request
to it. A key still not entered stays in `missingKeys`.

`fromUnsignedFile: true` marks a map that came in from a file Riki Maps did not sign. It travels
inside the signature of every later copy, and such a map is never published to the gallery.

### Several maps

A file with `maps` is a collection. Each entry is a whole map, exactly as it would be written
alone, signature and sidecars included:

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/mapson.schema.json",
  "_schemaVersion": 2,
  "maps": [ { /* a map */ }, { /* another */ } ],
  "rikiServiceProxies": { /* for every map; a map's own wins */ },
  "rikiHeaders": { /* the same */ }
}
```

A collection is `_schemaVersion` 2 and has at least one map. A writer with one map writes it
alone, as version 1, so readers that know only one map still open it.

### Value rules

- **Ids** are UUID strings such as `0834FFB7-67BA-4327-87F2-E18AEE11B2FC`. Either case works.
- **Pictures** (`iconPicture`, `imageData`) are standard base64 with padding.
- **Dates** are numbers: seconds since 2001-01-01T00:00:00Z.
- **Integers** (zooms, counts, bytes) must be whole numbers. `18.5` is refused.
- **Enums** (`role`, `format`, `overlay`, …) are closed. A value outside the list makes
  the whole file unreadable.
- **Optional means absent.** Leave a key out instead of writing `null`.
- **Unknown keys are allowed** and readers ignore them. A reader that re-exports a file
  may drop them.

### Signing is optional

`_signature` is optional. Riki Maps signs its own exports with a keyed hash so its import
sheet can say *"Verified · exported by Riki Maps"*. The mark is a UI hint, not security.

- A file without `_signature` is fully valid. It imports normally, just without the
  badge. Other writers should leave the key out.
- Any change to a signed file breaks the mark. The file still imports, only as
  unverified, so an editor should remove `_signature`.
- The signature covers the map, including `$schema`. It excludes `_schemaVersion`,
  `_signature` and the `riki*` sidecars (`rikiSharedFeature`, `rikiServiceProxies`,
  `rikiHeaders`), so those can change without touching it.
- In a collection each map carries its own signature; a collection is verified only when
  every map in it is.

### Versioning

- `_schemaVersion` is the format version. If it is missing, the file is version 0 (written
  before versioning), which reads the same as 1. A collection is 2.
- Adding an optional key does **not** change the version.
- The version goes up only when an older reader would misread a file. That change gets
  a new `schema/vN/` file. A reader must refuse a version newer than it knows instead of
  guessing, and Riki Maps does.
- `$schema` names the schema a file follows. It is optional; writers should set it.

## servson

Servers + JSON. A `.servson` holds one or more saved map servers instead of maps: their
addresses, kinds, request settings, their subservers (Esri folders and the services in them, to
any depth), and everything they published when last read (layers, facts, zooms, bounds), each
with the time of that read. With credentials when the writer chooses. It is a mapson extension: its schema
reuses mapson's `$defs` by relative `$ref`.

| | |
|---|---|
| Schema | [`schema/v1/servson.schema.json`](schema/v1/servson.schema.json) |
| Schema URL | `https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/servson.schema.json` |
| Examples | [`examples/minimal.servson`](examples/minimal.servson), [`examples/full.servson`](examples/full.servson) |
| Media | UTF-8 JSON, extension `.servson`, UTI `com.rikimaps.servson` |

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/servson.schema.json",
  "_schemaVersion": 1,
  "exportedAt": 812400000,
  "includesCredentials": false,
  "servers": [ /* in the writer's order */ ],
  "rikiHeaders": { /* host → header → value, only when includesCredentials */ },
  "rikiServiceProxies": { /* host → proxy prefix */ }
}
```

| Object | Required keys |
|---|---|
| root | `exportedAt` `includesCredentials` `servers` |
| server (`servers[]`) | `id` `name` `kind` `url` `headerNames` `symbol` `format` `maxZoom` `attribution` `allowsOffline` `layers` `facts` `addedAt` |
| layer (`layers[]`) | `id` `name` `supportsQuery` |
| service (`publishedServices[]`, `held[]`) | `id` `name` `type` `isFolder` `isDrawn` `layers` `facts` `held` `summary` |
| fact | `name` `value` |

`kind` is one of `arcgis` `tilejson` `tiles` `mapproxy` `api`. The value rules above apply.

A layer with `addedByHand` true was typed in by the user rather than published by the server.
It has its own `template` (or an Esri `number`), and a reader keeps it when it reads the server again.

**Credentials are the writer's choice.** With `includesCredentials` false, the file has no
`rikiHeaders`. Query keys such as `token`, `key` or `api_key` are also removed from every
address. Header *names* stay, so the reader knows which values it must supply. A reader should
name the hosts whose keys a file carries before importing it. It should also never replace a
value the user already holds.

## mapspack

Maps + pack: maps with the data they downloaded, as a folder. Its `map.mapson` is a mapson, one
map or several; beside it are each layer's tiles and the files its layers read (features,
GPX, GeoJSON, MBTiles…), and `package.json` says which belongs to which layer.

| | |
|---|---|
| Schema | [`schema/v1/mapspack.schema.json`](schema/v1/mapspack.schema.json), for `package.json` |
| Example | [`examples/huts.mapspack/`](examples/huts.mapspack) |
| Media | a folder, extension `.mapspack`, UTI `com.rikimaps.mapspack` (a package: Files shows one item) |

```
map.mapson          the maps, a mapson
package.json        which file belongs to which layer
<layer>.pmtiles     one per tile store, named after the layer that first reads it
files/<name>        files the layers read
```

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/skifahrer/schemas/master/schema/v1/mapspack.schema.json",
  "version": 1,
  "items": [
    { "layerID": "…", "cacheKey": "…", "tiles": "Trails.pmtiles", "files": [] },
    { "layerID": "…", "cacheKey": "…", "files": ["files/huts.geojson"] }
  ]
}
```

- `layerID` is a layer's `id` in any map of `map.mapson`.
- Layers that read the same store, in one map or across maps, name the same `tiles`.
- Every path `package.json` names must be in the mapspack.
- A reader refuses a `version` newer than it knows.

A folder is awkward to send, so a mapspack travels as an archive: a mapszip or a mapsaar. Both
unpack to the same mapspack.

## mapszip

Maps + zip: a mapspack in one file. Despite the name it is not a ZIP archive but a small
container of its own: a reader finds `map.mapson` at the front without unpacking the rest.

| | |
|---|---|
| Schema | [`schema/v1/mapszip.schema.json`](schema/v1/mapszip.schema.json), for the manifest |
| Examples | [`examples/minimal.mapszip`](examples/minimal.mapszip), [`examples/huts.mapszip`](examples/huts.mapszip) |
| Media | binary, extension `.mapszip`, UTI `com.rikimaps.mapszip` |

```
"RKZS"          4 bytes, magic
version         1 byte: 2 (1 is still read: every entry packed, no `stored`)
manifest size   4 bytes, unsigned, big-endian
manifest        UTF-8 JSON, the schema above
payload         each entry's bytes, in manifest order, nothing between or after
```

```jsonc
{ "entries": [
  { "path": "map.mapson", "size": 1520, "compressedSize": 702, "sha256": "…" },
  { "path": "package.json", "size": 310, "compressedSize": 190, "sha256": "…" },
  { "path": "Trails.pmtiles", "size": 9000000, "compressedSize": 9000000,
    "sha256": "…", "stored": true },
  { "path": "files/huts.geojson", "size": 277, "compressedSize": 190, "sha256": "…" }
] }
```

- Each entry is a file of the mapspack, at its path there. `map.mapson` and `package.json` are
  required and come first.
- A reader refuses a path that is absolute or holds `..`.
- An entry is LZFSE-compressed unless `stored` is true. Writers store what is already compressed
  (`.pmtiles`, images, `.zip`, `.gz`). `size` and `sha256` describe the unpacked bytes.
- [`tools/pack-mapszip.py`](tools/pack-mapszip.py) packs a mapspack folder with every entry
  stored, which needs no LZFSE.

## mapsaar

Maps + aar: a mapspack as a compressed [Apple Archive](https://developer.apple.com/documentation/applearchive).
Any Mac unpacks it with `aa extract -i Huts.mapsaar -d Huts.mapspack`, and the layers' tiles come
out as plain `.pmtiles` files that other tools open. It has no schema of its own: what comes out
is a mapspack.

| | |
|---|---|
| Media | Apple Archive (LZFSE), extension `.mapsaar`, UTI `com.rikimaps.mapsaar` |

## maps.json

The region catalog [skifahrer/maptiles](https://github.com/skifahrer/maptiles) publishes and Riki
Maps downloads from: countries, their regions and subregions, the mountains category with its
ranges, and each one's packages with a download per container format.

| | |
|---|---|
| Schema | [`schema/v1/maps.schema.json`](schema/v1/maps.schema.json) |
| Example | [`examples/maps.json`](examples/maps.json), an excerpt |
| Media | UTF-8 JSON, `maps.json` (`maps-test.json` for the pipeline's quick tests) |

```jsonc
{
  "_updated_at": "2026-10-01T09:35:02Z", "_updated_ts": 1790847302,
  "slovensko": { "name": "Slovakia", "regions": {
    "banskobystricky": { "bbox": [18.46, 48.035, 20.49, 48.965], "maxzoom": 14,
      "maps": { "base": { "download": "…", "size": 167844433, "sha256": "…",
        "formats": { "aar": { "download": "…" }, "zip": { "download": "…" } } } },
      "subregions": { /* cut-outs, the same shape */ } } } }
}
```

- Keys starting with `_` are metadata; [`mountains`](#mountains) is the category of ranges; every
  other top-level key is a country.
- Every country, region and subregion has an [`id`](#region-ids), unique across the catalog.
- `name` is what the app shows: a country in English (`Slovakia`), a region or subregion in its
  own language (`Banskobystrický kraj`, `Niederösterreich`).
- A package (`maps.<id>`) and each of its `formats` need `download`; everything else is optional.
- A package's top mirrors one of its formats, the ZIP where there is one, for older readers.
- `min_app_version` on a package (`"1.2"`, `"1.2.3"`) is the oldest app that can display it; older
  apps don't offer it. Absent, any app can.
- Dates are ISO 8601 UTC strings, with the same instant as Unix seconds in `*_ts`.
- Unknown keys are allowed. The pipeline validates every catalog it writes against this schema.

### Mountains

The top-level `mountains` is no country but a category of its own: under `ranges`, one range each,
in more detail than the regions carry — 2.5 m contours, rocks and a height model from the 1 m
LiDAR, roads and paths, and aerial photos of summer and winter. A range has the shape of a region
(`bbox`, zooms, `tiles`, `maps`), with only its own packages (`contours`, `rocks`, `terrain`,
`roads`, `paths`, `aerial_summer`, `aerial_winter`), and `country`, the country key whose data it
is made of. It needs no base map: it is drawn alone, or over the regions it crosses, in their
place where it has data. A range may cross a region or a state border, which is why it belongs
to no country.

```jsonc
"mountains": { "id": "mountains", "name": "Mountains",
  "ranges": {
    "vysoke_tatry": { "id": "mountains-vysoke_tatry", "name": "Vysoké Tatry",
      "country": "slovensko", "bbox": [19.9, 49.09, 20.32, 49.25], "contour_interval": 2.5,
      "maps": { "terrain": { "download": "…" }, "roads": { "download": "…" },
                "aerial_summer": { "download": "…" } } } } }
```

Its id is `mountains` and its key, joined by `-`, unique with the region ids. Catalogs written
before the category listed ranges under their country's `mountains` (`slovakia-vysoke_tatry`);
a reader takes those as ranges of that country.

### Region ids

Keys under `regions` are unique only within their country. The `id` is unique across the whole
catalog: the region's path on [download.openstreetmap.fr](https://download.openstreetmap.fr/extracts/)
below the continent, one piece per folder, joined by `-`. A `-` inside an osm.fr name becomes `_`,
so `-` only ever separates levels.

| osm.fr extract | id |
|---|---|
| `europe/slovakia-latest.osm.pbf` | `slovakia` |
| `europe/slovakia/banskobystricky-latest.osm.pbf` | `slovakia-banskobystricky` |
| `europe/france/rhone_alpes/savoie-latest.osm.pbf` | `france-rhone_alpes-savoie` |
| `north-america/us-west/california-latest.osm.pbf` | `us_west-california` |
| `russia/central_federal_district-latest.osm.pbf` | `russia-central_federal_district` |

A subregion (a cut-out) adds its key to its region's id: `slovakia-presovsky-pieniny`; a range
adds its key to the category's: `mountains-vysoke_tatry`. What osm.fr doesn't publish takes a name
of its own (`world`). OpenStreetMap has no such id of its own: a
boundary relation's number is unique but opaque, and ISO 3166-2 codes cover only official
subdivisions, not osm.fr's groupings or cut-outs. `tools/validate.py` refuses a catalog that
uses one id twice.

## Traffic signs

[skifahrer/traffic-signs](https://github.com/skifahrer/traffic-signs) keeps road signs by what
they mean, one folder per sign and one per country inside it:

```
signs/<category>/<sign>/<sign>.json                       the names
signs/<category>/<sign>/<country>/<sign>-<country>.json   one country's sign
signs/<category>/<sign>/<country>/<sign>-<country>.svg    its image
```

| Value | Rule |
|---|---|
| `category` | one of `warning` `regulatory` `information` `additional-panel` `traffic-device` `traffic-signal` |
| `sign` | English, lowercase, single hyphens: `bend-left`, `speed-limit-50`, `maximum-weight-3-5t` |
| `country` | ISO 3166-1 alpha-2, lowercase (`sk`), or ISO 3166-2 for a region (`us-ca`) |
| years (`valid_until`) | whole numbers: the last year a sign or image was known to be in use |

### One country's sign

| | |
|---|---|
| Schema | [`schema/v1/sign.schema.json`](schema/v1/sign.schema.json) |
| Example | [`examples/danger-sk.sign.json`](examples/danger-sk.sign.json) |

```jsonc
{
  "sign": "danger", "category": "warning", "country": "sk",  // the same as its path
  "code": "101",                                              // the national code
  "image": { "file": "danger-sk.svg", "sha1": "f3c1…", "source": "https://commons.wikimedia.org/wiki/File:…",
             "author": "…", "license": "Public domain", "license_url": null },
  "valid_until": 2026,                                        // only once it left its source page
  "archived": [ { "file": "danger-sk-archived-2026.svg", /* the image's keys */ "valid_until": 2026 } ],
  "source": { "pipeline": "sk-wikipedia", "page": "https://sk.wikipedia.org/wiki/…", "file": "101 Nebezpečenstvo.svg" }
}
```

| Object | Required keys |
|---|---|
| root | `sign` `category` `country` `code` |
| `image` | `file` `sha1` `source` `author` `license` `license_url` (the last three may be `null`) |
| `archived[]` | `file` (`null` when no file was kept) `valid_until` |
| `source` | `pipeline` `page` `file` |

`image` is absent until the image is downloaded, and after the sign left its page.

### A sign's names

| | |
|---|---|
| Schema | [`schema/v1/sign-names.schema.json`](schema/v1/sign-names.schema.json) |
| Example | [`examples/danger.sign-names.json`](examples/danger.sign-names.json) |

```json
{ "en": "Give way", "de": "Vorfahrt gewähren", "en-GB": "Give way", "en-US": "Yield" }
```

Shared by every country with the sign. `en` is required and comes first. Keys are ISO 639-1
codes; a second country with its own wording in a language adds its region (`de-AT`,
`en-US`, `en-US-CA` for a region of a country). Nothing else may be in the file.

### The viewer's data.json

| | |
|---|---|
| Schema | [`schema/v1/signs-data.schema.json`](schema/v1/signs-data.schema.json) |
| Example | [`examples/viewer.signs-data.json`](examples/viewer.signs-data.json) |

Built from `signs/` by `python3 -m viewer`: `categories` (folder → label), `countries` (code →
name, language, and `region_of` for a region), `groups` (continents and groups of countries
to compare), and `signs`, each with its `names` and per country its `code`, `image` (a path
from the site root), licence, author, source, `valid_until` and `archived` images. A variant
(`crosswind-from-left`) names its sign in `variant_of`; the sign lists it in `variants`.

To check a whole checkout, every file against its schema and its path:

```sh
tools/validate.py --signs ../traffic-signs/signs
```

## Validating

```sh
pip install jsonschema
tools/validate.py my-map.mapson my-servers.servson my-map.mapszip maps.json
```

Each file is checked against the schema its name says: its extension, `maps.json` or
`*.maps.json` for the catalog, `package.json` or `*.package.json` for a mapspack manifest,
`*.sign.json`, `*.sign-names.json` and `*.signs-data.json` for traffic sign files. A
folder is read as a mapspack. A mapszip is read as a container (magic, version, sizes, every
entry's sha256) and then as the mapspack it holds; packed entries need `pip install pyliblzfse`.
A `.mapsaar` is unpacked with `aa`, so only on a Mac.

Any 2020-12 validator works, for example Ajv: `new Ajv2020().compile(schema)` from
`ajv/dist/2020`. For servson, mapspack and maps.json, `addSchema(mapson)` first: they `$ref` its
`$defs`; for signs-data, `addSchema(sign)`. The schemas match what Riki Maps' decoders accept, so a file that passes imports there.
`tests/valid/` and `tests/invalid/` hold the edge cases that CI checks.

In an editor, map `*.mapson` and `*.servson` to JSON. VS Code then picks the schema up from the
file's `$schema` key.

### Pulling the schemas

Nothing copies these files. Riki Maps clones this repository into `.build/schemas` for its
tests (`tools/fetch-schemas.sh`); maptiles checks it out in the workflow that writes `maps.json`.
Pin a commit or tag there to hold a version.

## Security

Riki Maps asks on every export whether keys go with the file, for every format. Without them, it leaves out
`rikiHeaders` and the query keys in addresses, and names them in `access.missingKeys`, never
their values. A map sent to the gallery always goes without them.

A `.mapson` can carry `rikiHeaders`, which are header values such as API keys for the
map's own layers. It can also carry `rikiServiceProxies`. Readers should use either
only for hosts the map's own layers reach, and should show them to the user before
importing.
