FROM gemma4:e4b

PARAMETER temperature 0.1
PARAMETER num_ctx 32768

SYSTEM """You are an expert on the Cross-Domain Interoperability Framework (CDIF).
Your task is to answer any questions regarding CDIF, structure, architecture, and implementations.
Use the following official CDIF documentation to ground your answers:

### Source Document: PascalFeedback/CDIF_for_curators.md

# Aligning with the Cross-Domain Interoperability Framework (CDIF): A Guide for Data Managers and Metadata Curators

The **Cross-Domain Interoperability Framework (CDIF)** is a coordinate standard developed under the CODATA Decadal Programme. It provides a set of metadata implementation recommendations designed to support the **F.A.I.R. (Findable, Accessible, Interoperable, Reusable)** data principles across domain boundaries. 

Rather than inventing a new metadata standard, CDIF profiles and constraints leverage existing, widely adopted metadata standards (including **schema.org, W3C DCAT, DDI-CDI, W3C SKOS, W3C PROV-O, and RO-Crate**) to make digital resources machine-actionable, discoverable, and easily integrated.

This document serves as an onboarding guide for **Data Managers** and **Metadata Curators** seeking to align their repositories, datasets, and vocabularies with the CDIF specification.

---

## 1. The Seven CDIF Profiles: At a Glance

CDIF is structured as a modular suite of profiles. Depending on your data type, access mechanisms, and organizational needs, you may align with some or all of these profiles.

| Profile Name | Conformance URI | Core Purpose | Target Domain / Use Cases |
| :--- | :--- | :--- | :--- |
| **1. Core Profile** | `https://w3id.org/cdif/core/1.0` | Establishes baseline dataset identity, access rights, and distribution endpoints. | All datasets and digital resources. |
| **2. Discovery Profile** | `https://w3id.org/cdif/discovery/1.0` | Adds granular spatial, temporal, and variable descriptions to make data findable. | Cross-domain cataloging, search indexes, spatial-temporal queries. |
| **3. Data Description Profile** | `https://w3id.org/cdif/data_description/1.0` | Details the internal structure of values, mapping physical columns to semantic variables. | Tabular files (CSVs), scientific data formats, statistical datasets. |
| **4. Data Structure Profile** | `https://w3id.org/cdif/data_structure/1.0` | Models structural layout types (Wide, Long, Dimensional, Key-Value) using DDI-CDI. | Advanced data integration pipelines, multidimensional data cubes. |
| **5. Codelist Profile** | `https://w3id.org/cdif/codelist/1.0` | Standardizes controlled vocabularies and taxonomies using bidirectional SKOS hierarchies. | Controlled vocabularies, classification schemes, code registries. |
| **6. Provenance Profile** | `https://w3id.org/cdif/provenance/1.0` | Tracks data lineage, acquisition methods, and step-by-step processing workflows. | Pipelled data, sensor networks, reproducible scientific workflows. |
| **7. Manifest Profile** | `https://w3id.org/cdif/manifest/1.0` | Standardizes flat packaging and serialization formats for data transport. | Data repositories (Zenodo, Dataverse), AI training sets (Croissant format). |

---

## 2. Why Align? Benefits of CDIF Compliance

Aligning with CDIF offers substantial benefits to data repositories, research networks, and archiving systems:

*   **Silo-Free Cross-Domain Discovery:** Historically, social sciences, health sciences, and environmental monitoring systems used incompatible metadata standards (e.g., DDI, HL7 FHIR, and ISO 19115). CDIF maps these domain-specific schemas into a unified, lightweight JSON-LD representation built on schema.org, allowing datasets from different origins to be indexed by global search engines and cross-domain catalogs simultaneously.
*   **Machine-Actionable Data Integration:** CDIF goes beyond typical descriptive cataloging. By specifying physical column-to-variable mappings and structural layouts (e.g., Wide vs. Long formats), data integration software can programmatically read, align, and merge datasets without human intervention or manual recoding.
*   **Ambiguity Resolution (Sentinel vs. Substantive Values):** CDIF prevents data corruption in automated pipelines by strictly separating *substantive values* (valid, meaningful measurements) from *sentinel values* (missing data flags, non-responses, or instrumentation errors). This ensures automated analytical tools do not compute sensor codes (like `-9999` or `999`) as actual physical measurements.
*   **Workflow Reproducibility & Auditing:** Curating provenance metadata using W3C PROV-O and RO-Crate models creates a clear chain of custody. Users can audit how the data was collected, what software or instruments were used, and exactly how the data was transformed.
*   **Semantic Consistency:** The Codelist profile ensures classification codes maintain their meaning over time and across systems by enforcing explicit, bidirectional hierarchies (`skos:broader` and `skos:narrower`), preventing semantic drifts when translating vocabularies.
*   **AI Readiness and LLM/Agentic Integration:** Aligning datasets with CDIF profiles—particularly utilizing formats like MLCommons Croissant—makes resources instantly ready for AI ingestion. The clean structure, unambiguous semantic definitions, and structured primary keys enable Large Language Models (LLMs) and autonomous AI coding agents to automatically query, parse, and analyze datasets without requiring manual custom-built pipeline setup.

---

## 3. Information Gathering Checklist for CDIF Compliance

To prepare your dataset or repository for CDIF alignment, curators must gather and organize specific metadata elements. Below is the operational checklist of information to assemble prior to generating CDIF-compliant JSON-LD records.

### Checklists by Curation Category

```mermaid
graph TD
    classDef gather fill:#ede7f6,stroke:#5e35b1,stroke-width:2px;
    classDef check fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;

    C1["1. Core & Discovery Metadata"]:::gather
    C2["2. Structural Layout Details"]:::gather
    C3["3. Variable & Domain Mapping"]:::gather
    C4["4. Codelists & Vocabularies"]:::gather
    C5["5. Lineage & Workflow Records"]:::gather

    V["CDIF JSON-LD Record Generator"]:::check
    SHACL["SHACL / Schema Validator"]:::check

    C1 --> V
    C2 --> V
    C3 --> V
    C4 --> V
    C5 --> V
    V --> SHACL
```

#### Category 1: Core & Discovery Metadata (Core & Discovery Profiles)
*   [ ] **Resource Identifiers:** Globally unique, resolvable IRIs/URIs for the dataset (e.g., DOI URLs, Handles) to populate `@id` and `schema:identifier`.
*   [ ] **Metadata Provenance:** Unique identifiers, modification timestamps, and maintainer information for the metadata catalog record itself (to populate the nested `dcat:CatalogRecord` under `schema:subjectOf`).
*   [ ] **Access & Rights:** A machine-readable license URL (e.g., Creative Commons URIs) or a URL pointing to explicit conditions of access.
*   [ ] **Access Methods:** The landing page URL OR direct file download URLs (`schema:DataDownload`) or API end-point protocols and restrictions (`schema:WebAPI` using OpenAPI specs).
*   [ ] **Spatial Bounds:** Coordinate bounding boxes or centroids mapped strictly in **decimal degrees under the WGS 84 datum** (e.g., `schema:spatialCoverage` -> `schema:geo`).
*   [ ] **Temporal Extents:** Calendar times represented as ISO 8601 strings. For non-calendar periods (e.g., geological eras, cyclical schedules), define the start and end boundaries using OWL-Time (`time:ProperInterval`).
*   [ ] **Dataset Citation Info:** Ordered creator lists (using ORCIDs for researchers and ROR IDs for organizations) and funding grants (with funding body IDs).

> [!WARNING]  
> **Coordinate Projection Errors:** CDIF validation will fail if spatial boundaries are expressed in local projections (e.g., UTM grid zones or EPSG codes). You must transform all geographic coordinates into decimal degrees on WGS 84 (EPSG:4326) prior to compliance checks.

#### Category 2: Structural Layout Details (Data Structure & Manifest Profiles)
*   [ ] **Dataset Physical Format:** The mime-types, character set (e.g., `UTF-8`), and total content sizes of all data distributions.
*   [ ] **Physical Layout Type:** Classification of the dataset's structural style:
    *   *Wide:* Rows represent observation units, columns represent distinct variables.
    *   *Long:* Rows stack variable names and values vertically (requiring identification of descriptor and value columns).
    *   *Dimensional:* Multidimensional arrays or data cubes (e.g., NetCDF, HDF5, SDMX).
    *   *Key-Value:* Schemas using key-value pair distributions.
*   [ ] **Delimited Text Constraints:** For tabular data (e.g., CSVs), confirm the column delimiter (comma, tab, semicolon) and whether a header row is present (mapping W3C CSVW parameters).
*   [ ] **Primary Keys:** Identify which column or ordered list of columns uniquely identify each row (to construct `cdif:hasPrimaryKey`).
*   [ ] **Packaging Organization:** Determine if files are served independently or zipped into archives. (Archive files require cataloging internal components using `schema:hasPart` referencing `schema:MediaObject` nodes).

#### Category 3: Variable & Value Domain Mapping (Data Description Profile)
*   [ ] **Column-to-Variable Mapping:** Map every raw column name or hierarchical array path back to its semantic variable definition. Note the 0-based index of each column.
*   [ ] **Physical Data Types:** Identify the physical type for each column (e.g., `float`, `integer`, `string`, `datetime`).
*   [ ] **Substantive Domains:** For numerical or measurement columns, define the valid, meaningful value ranges (minimum and maximum observed values) and the unit of measure (e.g., Celsius, meters).
*   [ ] **Sentinel Domains:** Document the specific codes representing missing values, refusals, or system errors (e.g., identifying `-9999` as "Instrument Failure", `-1` as "Refused to Answer", or empty strings as "Not Collected").
*   [ ] **Concept Associations:** Associate each variable with a conceptual definition in a standard vocabulary or registry (e.g., linking a column representing "Air Temperature" to a WMO concept URI).

> [!IMPORTANT]  
> **Sentinel Value Domain Separation:** Do not mix sentinel/missing codes into the general variable range. You must compile a distinct list of sentinel values and map them to their specific semantic reasons so pipelines can filter them automatically.

#### Category 4: Codelists & Controlled Vocabularies (Codelist Profile)
*   [ ] **Vocabulary Identity:** A unique, resolvable URI for the vocabulary container (`skos:ConceptScheme`) and its human-readable title.
*   [ ] **Term Listings:** Unique URIs, codes/notations, preferred human labels, and semantic definitions for each individual term in the vocabulary (`skos:Concept`).
*   [ ] **Hierarchical Relationships:** Map parent-child relationships in **both directions**:
    *   Identify which concepts are the root/top concepts.
    *   For every concept, specify its parent concept (`skos:broader`).
    *   For every parent, specify its child concepts (`skos:narrower`).

> [!TIP]  
> **Bidirectional SKOS Hierarchies:** Many vocabulary databases export code trees unidirectionally (only from child to parent). Before aligning with the Codelist profile, ensure you run processing scripts to generate the inverse links (`skos:narrower`), as CDIF SHACL rules strictly require bidirectional declarations.

#### Category 5: Lineage & Workflow Records (Provenance Profile)
*   [ ] **Upstream Source Datasets:** Identifiers and descriptions of all input datasets used to generate the current resource.
*   [ ] **Workflow Methodology:** Step-by-step descriptions of the processing pipeline (e.g., standard workflow scripts, computational step scripts, or Galaxy pipelines).
*   [ ] **Computational Tooling:** Specific software names, container versions (Docker/Singularity hashes), Github repository tags, or API versions used in each execution step.
*   [ ] **Processing Parameters:** Configuration variables, environmental settings, or command-line flags supplied during runtime.
*   [ ] **Agents & Roles:** Identifiers for the people or organizational units executing the process, along with their roles (e.g., "Creator", "Data Curator", "Validator").

---

## 4. Understanding CDIF Validation

Once the required information has been gathered and serialized into JSON-LD, compliance is verified through a two-step process:

1.  **JSON Schema Validation:** Ensures the structural syntax of the JSON-LD is correct (e.g., correct JSON keys, data types, and array formats).
2.  **SHACL (Shapes Constraint Language) Validation:** Evaluates semantic rules directly on the graph structure. SHACL checks confirm requirements such as:
    *   Declaring conformance to the correct profiles in the `dcat:CatalogRecord`.
    *   Ensuring spatial bounds are numeric decimal coordinates.
    *   Ensuring `RepresentedVariables` carry domain parameters rather than repeating them on individual instance variables.
    *   Verifying that `skos:Concept` hierarchies are perfectly bidirectional.

By using the checklists in this guide, metadata curators can preemptively clean and structure their information, ensuring a smooth path to CDIF conformance and true cross-domain interoperability.

---


---
### Source Document: PascalFeedback/cdif_profile_elements.md

# CDIF Profile Element Master Index

This master index aggregates all metadata classes and properties defined across the 7 Cross-Domain Interoperability Framework (CDIF) profiles: **Core, Discovery, Data Description, Data Structure, Codelist, Provenance, and Manifest (Packaging)**.

---

## Master Element Reference Table

| Element (Class / Property) | Profile(s) | Type / Expected Value | Cardinality / Requirement | Description & Context |
| :--- | :--- | :--- | :--- | :--- |
| [`schema:Dataset`](https://schema.org/Dataset) | Core, Discovery, Data Description, Data Structure, Provenance, Manifest | Class | **Required** | The root entity representing the dataset or digital resource. |
| ↳ [`schema:identifier`](https://schema.org/identifier) | Core, Codelist | `string.uri` OR [`schema:PropertyValue`](https://schema.org/PropertyValue) | **Required (1)** | Unique, resolvable primary identifier (e.g. DOI URL, ORCID). |
| ↳ [`schema:name`](https://schema.org/name) | Core, Discovery, Codelist | `string` | **Required (1)** | Title or human-readable name of the entity. |
| ↳ [`schema:dateModified`](https://schema.org/dateModified) | Core, Codelist | `string` (ISO 8601) | **Required (1)** | Last update timestamp for the dataset or vocabulary. |
| ↳ [`schema:subjectOf`](https://schema.org/subjectOf) | Core, Manifest | [`dcat:CatalogRecord`](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record) | **Required (1)** | Links dataset to its metadata management record. |
| ↳ [`schema:license`](https://schema.org/license) | Core, Codelist | `string` OR `@id` reference | **Conditional Required** | Choice: supply `license` OR `conditionsOfAccess`. |
| ↳ [`schema:conditionsOfAccess`](https://schema.org/conditionsOfAccess) | Core, Codelist | `string` OR `@id` reference | **Conditional Required** | Choice: supply `license` OR `conditionsOfAccess`. |
| ↳ [`schema:url`](https://schema.org/url) | Core | `string.uri` | **Conditional Required** | Choice: supply landing page `url` OR a `distribution`. |
| ↳ [`schema:distribution`](https://schema.org/distribution) | Core, Data Description, Manifest | [`schema:DataDownload`](https://schema.org/DataDownload) OR [`schema:WebAPI`](https://schema.org/WebAPI) | **Conditional Required** | Choice: supply landing page `url` OR a `distribution` (1..*). |
| ↳ [`schema:description`](https://schema.org/description) | Core | `string` | Recommended (0..1) | Detailed summary of the dataset. Warns on check if missing. |
| ↳ [`schema:creator`](https://schema.org/creator) | Core | `@list` of `Person`/`Org` | Recommended (0..*) | Ordered list of creators/authors. Warns on check if missing. |
| ↳ [`schema:keywords`](https://schema.org/keywords) | Core | `string` or `DefinedTerm` | Optional (0..*) | Tags or terms classifying the resource. |
| ↳ [`schema:funding`](https://schema.org/funding) | Core | [`schema:MonetaryGrant`](https://schema.org/MonetaryGrant) | Optional (0..*) | Linked grant details and funding bodies. |
| ↳ [`schema:version`](https://schema.org/version) | Core | `string` or `number` | Optional (0..1) | Sortable version label of the dataset. |
| ↳ [`schema:inLanguage`](https://schema.org/inLanguage) | Core | `string` (ISO 639) | Optional (0..1) | Primary language of the content. |
| ↳ [`schema:datePublished`](https://schema.org/datePublished) | Core | `string` (ISO 8601) | Optional (0..1) | Date when the dataset was made public. |
| ↳ [`schema:sameAs`](https://schema.org/sameAs) | Core, Discovery | `string.uri` | Optional (0..*) | Alternate identifier URLs. |
| ↳ [`schema:relatedLink`](https://schema.org/relatedLink) | Core | [`schema:LinkRole`](https://schema.org/LinkRole) | Optional (0..*) | Links to publications, software, or tools. |
| ↳ [`schema:publishingPrinciples`](https://schema.org/publishingPrinciples) | Core | `string` OR `@id` reference | Optional (0..*) | Link to update policy/maintenance descriptions. |
| ↳ [`schema:additionalType`](https://schema.org/additionalType) | Core | `string` or `DefinedTerm` | Optional (0..*) | Secondary/semantic classification types. |
| ↳ [`prov:wasDerivedFrom`](https://www.w3.org/TR/prov-o/#wasDerivedFrom) | Core, Provenance | `@id` reference | Optional (0..*) | References upstream datasets used as input. |
| ↳ [`prov:wasGeneratedBy`](https://www.w3.org/TR/prov-o/#wasGeneratedBy) | Core, Provenance | [`prov:Activity`](https://www.w3.org/TR/prov-o/#Activity) | Optional (0..*) | Process or script that generated this dataset. |
| ↳ [`schema:variableMeasured`](https://schema.org/variableMeasured) | Discovery | [`schema:PropertyValue`](https://schema.org/PropertyValue) or [`cdi:InstanceVariable`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#InstanceVariable) | Optional (0..*) | List of variables (Discovery Properties or CDI Variables). |
| ↳ [`schema:spatialCoverage`](https://schema.org/spatialCoverage) | Discovery | [`schema:Place`](https://schema.org/Place) | Optional (0..*) | Geographic boundaries of dataset collection. |
| ↳ [`schema:temporalCoverage`](https://schema.org/temporalCoverage) | Discovery | `string` OR [`time:ProperInterval`](https://www.w3.org/TR/owl-time/#class-proper-interval) | Optional (0..*) | Temporal range (ISO 8601 interval or OWL interval). |
| ↳ [`schema:measurementTechnique`](https://schema.org/measurementTechnique) | Discovery | `string` or `DefinedTerm` | Optional (0..*) | Methodology used to collect values. |
| ↳ [`dqv:hasQualityMeasurement`](https://www.w3.org/TR/vocab-dqv/#dqv:hasQualityMeasurement) | Discovery | [`dqv:QualityMeasurement`](https://www.w3.org/TR/vocab-dqv/#dqv:QualityMeasurement) | Optional (0..*) | Measured data quality parameters. |
| [`dcat:CatalogRecord`](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record) | Core | Class | **Required** | Nested metadata management record. |
| ↳ [`schema:about`](https://schema.org/about) | Core | `@id` reference | **Required (1)** | Points back to the parent `schema:Dataset`. |
| ↳ [`dcterms:conformsTo`](http://purl.org/dc/terms/conformsTo) | Core, Manifest | `@id` reference | **Required (1..*)** | Conformance profile URIs (e.g. Core, Discovery). |
| [`schema:DataDownload`](https://schema.org/DataDownload) | Core, Data Description, Manifest | Class | **Required** | Digital distribution (file download). |
| ↳ [`schema:contentUrl`](https://schema.org/contentUrl) | Core | `string.uri` | **Required (1)** | Direct download URL. |
| ↳ [`schema:encodingFormat`](https://schema.org/encodingFormat) | Core | `string` | Optional (0..*) | MIME format of the file. |
| ↳ [`spdx:checksum`](http://spdx.org/rdf/terms#checksum) | Core | [`spdx:Checksum`](http://spdx.org/rdf/terms#Checksum) | Optional (0..1) | File integrity hash object. |
| ↳ [`csvw:delimiter`](https://www.w3.org/TR/tabular-metadata/#dfn-delimiter) | Data Description | `string` | **Required (1 for Tabular)** | Character separating values (e.g., `","`, `"\t"`). |
| ↳ [`csvw:header`](https://www.w3.org/TR/tabular-metadata/#dfn-header) | Data Description | `boolean` | **Required (1 for Tabular)** | Indicates if a header row is present in the file. |
| ↳ [`cdi:characterSet`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#PhysicalDataSet-characterSet) | Data Description | `string` | Optional (0..1) | Character encoding (e.g., `"UTF-8"`). |
| ↳ [`cdif:hasPhysicalMapping`](https://w3id.org/cdif/data_description/1.0) | Data Description | Array of mappings | **Required (1..* for maps)** | Column-to-variable structural mappings. |
| ↳ [`schema:hasPart`](https://schema.org/hasPart) | Manifest | Array of `MediaObject`/`Work` | Optional (0..*) | Files nested inside an archive distribution. |
| [`schema:WebAPI`](https://schema.org/WebAPI) | Core | Class | **Required** | Digital distribution (service-based API). |
| ↳ [`schema:serviceType`](https://schema.org/serviceType) | Core | `string` or `DefinedTerm` | **Required (1)** | Protocol standard identifying name (e.g. OpenAPI). |
| ↳ [`schema:termsOfService`](https://schema.org/termsOfService) | Core | `string` or `LabeledLink` | **Required (1..*)** | API access conditions/credentials. |
| ↳ [`schema:potentialAction`](https://schema.org/potentialAction) | Core | [`schema:Action`](https://schema.org/Action) | **Required (1..*)** | Executable API actions. |
| [`schema:Place`](https://schema.org/Place) | Discovery | Class | **Required (if spatial)** | Spatial boundary location. |
| ↳ [`schema:geo`](https://schema.org/geo) | Discovery | Point / Bounding Box | **Required (1)** | Geographic bounds in decimal degrees on WGS 84. |
| [`time:ProperInterval`](https://www.w3.org/TR/owl-time/#class-proper-interval) | Discovery | Class | **Required (if temporal)** | Non-standard calendar temporal bounds. |
| ↳ [`time:hasBeginning`](https://www.w3.org/TR/owl-time/#property-hasBeginning) | Discovery | `@id` or value | **Required (1)** | Start boundary of the interval. |
| ↳ [`time:hasEnd`](https://www.w3.org/TR/owl-time/#property-hasEnd) | Discovery | `@id` or value | **Required (1)** | End boundary of the interval. |
| [`cdi:InstanceVariable`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#InstanceVariable) | Data Description, Data Structure | Class | Optional (0..*) | A semantic variable populated in the dataset. |
| ↳ [`cdif:physicalDataType`](https://w3id.org/cdif/data_description/1.0) | Data Description | `string` | **Required (1..*)** | Physical representation data type (e.g., `float`). |
| ↳ [`cdi:takesSubstantiveValuesFrom`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#RepresentedVariable-takesSubstantiveValuesFrom) | Data Description | Value Domain | Optional (0..1) | Domain defining valid values. |
| ↳ [`cdi:takesSentinelValuesFrom`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#RepresentedVariable-takesSentinelValuesFrom) | Data Description | Value Domain | Optional (0..*) | Domain defining missing/refusal values. |
| [`cdi:DataStructure`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#DataStructure) | Data Structure | Class | **Required (if structure)** | Physical structural layout container. |
| ↳ [`cdi:has_DataStructureComponent`](http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/#DataStructure-has_DataStructureComponent) | Data Structure | Array of Components | **Required (1..*)** | Mapped component columns. |
| [`skos:ConceptScheme`](https://www.w3.org/TR/skos-reference/#ConceptScheme) | Codelist | Class | **Required** | The vocabulary scheme definition. |
| ↳ [`skos:prefLabel`](https://www.w3.org/TR/skos-reference/#prefLabel) | Codelist | `string` | **Required (1..*)** | Title/label for vocabulary scheme. |
| ↳ [`skos:hasTopConcept`](https://www.w3.org/TR/skos-reference/#hasTopConcept) | Codelist | Array of `@id` | **Required (1..*)** | Root terms in the taxonomy. |
| [`skos:Concept`](https://www.w3.org/TR/skos-reference/#Concept) | Codelist | Class | **Required** | Individual term/code in codelist. |
| ↳ [`skos:inScheme`](https://www.w3.org/TR/skos-reference/#inScheme) | Codelist | `@id` reference | **Required (1)** | Links term back to parent ConceptScheme. |
| ↳ [`skos:definition`](https://www.w3.org/TR/skos-reference/#definition) | Codelist | `string` | **Required (1..*)** | Semantic definition of term. |
| ↳ [`skos:broader`](https://www.w3.org/TR/skos-reference/#broader) | Codelist | `@id` reference | **Conditional Required** | Required (1..*) if term has parent term. |
| ↳ [`skos:narrower`](https://www.w3.org/TR/skos-reference/#narrower) | Codelist | `@id` reference | **Conditional Required** | Required (1..*) if term has child terms. |
| [`prov:Activity`](https://www.w3.org/TR/prov-o/#Activity) | Core, Provenance | Class | **Required** | Workflow run, processing event or acquisition step. |
| ↳ [`prov:used`](https://www.w3.org/TR/prov-o/#used) | Provenance | Array of `@id` | Optional (0..*) | Datasets/files consumed by the activity. |
| ↳ [`prov:wasAssociatedWith`](https://www.w3.org/TR/prov-o/#wasAssociatedWith) | Provenance | Array of `@id` (Person/Org) | Optional (0..*) | Agents (Person/Organization) running the activity. |
| ↳ [`schema:actionProcess`](https://schema.org/actionProcess) | Provenance | [`schema:HowTo`](https://schema.org/HowTo) | Optional (0..1) | Methodology workflow script template. |
| [`prov:Entity`](https://www.w3.org/TR/prov-o/#Entity) | Provenance | Class | **Required** | Artifacts generated or consumed by activities. |
| ↳ [`prov:wasGeneratedBy`](https://www.w3.org/TR/prov-o/#wasGeneratedBy) | Provenance | `@id` reference | Optional (0..1) | The activity that produced the entity. |
| ↳ [`prov:wasDerivedFrom`](https://www.w3.org/TR/prov-o/#wasDerivedFrom) | Provenance | Array of `@id` | Optional (0..*) | Direct lineage reference to parent inputs. |


---
### Source Document: PascalFeedback/compliance_challenges-smr.md

# CDIF Profile Compliance & Implementation Challenges Report

This report analyzes the compliance requirements, required elements, and practical implementation barriers across the Cross-Domain Interoperability Framework (CDIF) profiles: **Core, Discovery, Data Description, Data Structure, Codelist, Provenance, and Manifest (Packaging)**.

---

## 1. Compliance Architecture Overview

CDIF enforces compliance using a two-stage validation workflow:
1.  **JSON Schema Validation:** Structural validation (closed-world) verifying that required properties, array structures, and JSON keys are correctly structured. This requires JSON-LD framing to shape the RDF graph into a normalized tree before validation.
2.  **SHACL (Shapes Constraint Language) Validation:** Semantic validation (open-world) checking cross-node constraints, vocabulary checks, and conditional logic directly on the RDF graph.

---

## 2. Profile-by-Profile Compliance Analysis

### A. Core Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/core/1.0`
*   **Core Required Elements:** `@id`, `@type` (must include `"Dataset"`), `schema:name` (meaningful title), `schema:identifier` (resolvable URI or `PropertyValue`), `schema:dateModified`, `schema:subjectOf` (CatalogRecord linkage), choice of rights (`license` or `conditionsOfAccess`), choice of download (`url` or `distribution`).

#### Practical Compliance Barriers & Challenges:
*   **Ambiguity in Metadata Provenance:** Separation of the metadata record itself from the resource it describes is achieved via a nested `dcat:CatalogRecord`. Legacy search indexing engines (like Google Dataset Search or standard catalogs) do not Monatively parse this nested structure and often conflate the catalog record's modification date (`schema:sdDatePublished`) with the dataset's modification date (`schema:dateModified`).

> ⚠️ **[REVIEW]** this approach solves the long standing ambiguity on what schema:dateModified actually qualifies. If a client doesn't parse the CatalogRecord, no information will be misinterpreted, but the update date for the metadata node would be lost. 


*   **Access Rights Structure:** Many repositories do not provide a machine-actionable license URI or formal access conditions, but instead provide long unstructured legal text blocks. Mapping these into a `LabeledLink` (`schema:CreativeWork`) requires manual curation or complex text extraction.

> ⚠️ **[REVIEW]**  If the repository only provides unstructured legal text, complex text extraction is going to be required, no matter where you put it in the JSON. In cdifCore this text would be inserted as text in the schema:conditionsOfAccess, not in a LabeledLink; the schema allows either option (or just an @id object reference to something).

---

### B. Discovery Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/discovery/1.0`
*   **Discovery Required/Conditional Elements:** `schema:variableMeasured` (required for datasets), `schema:spatialCoverage` (required if geographically bounded), `schema:temporalCoverage` (required if temporally bounded).

#### Practical Compliance Barriers & Challenges:
*   **Geographic Coordinate Standardisation:** Spatial bounds must be defined in decimal degrees using the WGS 84 datum. Most legacy spatial metadata records (e.g. from ISO 19115 or local GIS databases) store extents in custom UTM zones, local projections, or named projections (e.g. EPSG codes), requiring coordinate transformation pipelines to pass validation.

> ⚠️ **[REVIEW]** "Most legacy spatial metadata records..." -- what's the evidence?  all the ISO19115 profiles I've worked on require WGS84 decimal degrees-- this is a requirement for interoperability (like speaking the same language).  Yes the data provider has to do a SRS conversion, but if they're using any modern GIS system, that's a trivial operation; metadata harvesters on the other hand are generally not equipped with SRS transformation capabilities.


*   **Temporal Extents (OWL Time):** Geologic time, cyclicity, or named ordinal eras must be mapped using `time:ProperInterval`. Representing geological boundaries (e.g. "Jurassic") in a machine-readable format that crosswalks cleanly with calendar time is a massive semantic challenge.

> ⚠️ **[REVIEW]**  the whole point is to enable temporal systems based on named ordinal eras for time positions that predate any calendar, and might not have known numeric temporal positions.  There are ordinal eras that overlap with calendars (e.g. 'reign of Henry VIII).


*   **Variable List Extraction:** Extracting conceptual variables out of raw data distributions (such as CSV file headers) to populate `schema:variableMeasured` is highly labor-intensive and lacks standard vocabulary mapping, leaving them as plain strings that fail advanced semantic queries.

> ⚠️ **[REVIEW]** The perfect is the enemy of the good....  Extracting column headers from text based tabular formats files is generally pretty easy; yes, we might just end up with an instance variable that has a label, and yes, sometimes people create tables with headers that are nonsense, but in general between inspecting the content of the columns in the table, and the label string provided, we can provide useful, if not perfect information that will have an obvious path for improvement.

---

### C. Data Description Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/data_description/1.0`
*   **Data Description Required Elements:** `cdi:InstanceVariable` typing on variables, `cdif:physicalDataType` (array on variables, string on mappings), physical mapping (`cdif:hasPhysicalMapping` with `cdif:index` or `cdif:locator` and `cdif:formats_InstanceVariable` references).

#### Practical Compliance Barriers & Challenges:
*   **Physical Columns to Semantic Variables Mapping:** Physical column labels in raw files (e.g. `tmp_c_1`) must be explicitly mapped to semantic `InstanceVariable` definitions. If a dataset contains hundreds of abbreviated columns, creating these physical mapping nodes (`cdif:hasPhysicalMapping`) requires custom automated scripts.

> ⚠️ **[REVIEW]** I've not found this to be a problem that claude-code can't solve pretty quick.

*   **Value Domain Isolation:** CDIF requires separating substantive values from sentinel (missing/fill) codes (such as sensor `-9999` fill values or survey refusal codes) using `cdif:SubstantiveValueDomain` and `cdif:SentinelValueDomain`. Standard repository exports typically intermingle these inside data columns, requiring manual dataset inspection to extract and structure them.

> ⚠️ **[REVIEW]**  I agree-- this is an important point; we need a simpler way to represent value enumerations that include both sentinel and substantive values. See [value domains-- sentinel values should be indicated by a 'type'
 ](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/issues/1)

*   **Primary Key Modeling:** Multi-column keys require assembling `cdif:hasPrimaryKey` with ordered `cdi:ComponentPosition` nodes. Traditional repository metadata (such as Dataverse or Zenodo) does not export primary key constraints, necessitating custom post-processing to derive them.

> ⚠️ **[REVIEW]**  that is probably the case, but how often do we have to deal with multi-column keys. In the examples I've worked with so far, I havn't even found a primary key definition...  the IdentifierComponent usually fills the role. 

---

### D. Data Structure Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/data_structure/1.0`
*   **Data Structure Required Elements:** `cdi:isStructuredBy` pointing to `cdi:DataStructure` on distributions, subtyped layout classes (Wide, Long, Dimensional, Key-Value), and reusable represented variables (`cdi:RepresentedVariable`).

#### Practical Compliance Barriers & Challenges:
*   **Modeling Complexity for Long Layouts:** Long-format datasets (where variable names and values are stacked in rows) require matching `cdi:VariableDescriptorComponent` to `cdi:VariableValueComponent`. This is a highly abstract structural modeling paradigm that standard developers struggle to implement correctly.

> ⚠️ **[REVIEW]** I don't doubt it! Is there a better way?


*   **Deep JSON-LD Nesting:** By lifting value domains and units to `cdi:RepresentedVariable` and linking them via `cdif:uses`, the JSON-LD document becomes deeply nested and extremely difficult to inspect or author manually.

> ⚠️ **[REVIEW]** that's only required if one is creating a standAlone structure definition, and yes that reusability generates complexity. Fortunately, there shouldn't be much (if any) manual editing of this kind of metadata.

---

### E. Codelist Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/codelist/1.0`
*   **Codelist Required Elements:** `skos:ConceptScheme` defining the vocabulary, and `skos:Concept` defining terms. Must provide preferred labels and definitions.

#### Practical Compliance Barriers & Challenges:
*   **Strict Bidirectional Hierarchy:** CDIF mandates that all hierarchical relationships be defined in both directions: parent concepts must link to children via `skos:narrower`, and child concepts must link back via `skos:broader`. Standard vocabulary management systems (like PoolParty, VocBench, or Protégé) often export hierarchies unidirectionally, causing exported codelists to fail CDIF SHACL rules.

> ⚠️ **[REVIEW]** A topic for discussion.  In order to only use skos:broader, in JSON-LD the vocabulary has to be represented a graph, with a node for each concept.  To generate a JSON-compatible (hierarchical, nested) representation, you have to go from conceptScheme-->topConcept-->narrower-->other concept.   We were given the requirement that skos:broader relations are required if the vocab is hierarchical.  The ramification is that both broader and narrower are required.   Fortunately its a pretty easy sparql insert to get both relations in. 


*   **Handling Array Exceptions:** Because Codelists do not enforce strict array wrapping for repeatables (to comply with standard SKOS serialization), client parsing software must write custom conditional checks to handle both single string values and arrays.


> ⚠️ **[REVIEW]**  Interesting, I wasn't aware strict array wrapping for repeatables is standard SKOS serialization; the schema I looked at allow string or array values. In the other CDIF schema we do require  array wrapping for repeatables.  ?should we revise the schema?

---

### F. Provenance Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/provenance/1.0`
*   **Provenance Required Elements:** `prov:Activity` subtyped as `schema:Action`, `prov:used` (inputs), `prov:wasAssociatedWith` (performers), `prov:Entity` subtyped as `schema:Dataset`, and `prov:wasGeneratedBy`.

#### Practical Compliance Barriers & Challenges:
*   **Workflow Granularity Bloat:** Pipeline tools (such as Snakemake, Nextflow, or Galaxy) produce highly granular execution logs. Converting every command step into a `prov:Activity` linked by `prov:wasInformedBy` results in massive metadata files that can overwhelm search indexers.
*   **Actor Identification:** Automated processing runs are typically executed by system accounts, service workers, or virtual nodes rather than individuals. Mapping these to valid schema.org `Person` or `Organization` nodes with unique identifiers (like ROR or ORCID) is often impossible without inventing dummy records.

> ⚠️ **[REVIEW]**  noted. this prov profile is a draft, not part of the release packages.

---

### G. Manifest (Packaging) Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/manifest/1.0`
*   **Manifest Required Elements:** Flat `@graph` structure in RO-Crate, metadata descriptor `ro-crate-metadata.json`, root dataset remapped to `"./"`.

#### Practical Compliance Barriers & Challenges:
*   **Translation Overhead:** Converting between nested trees (normal CDIF) and flat graphs (RO-Crate) requires running JSON-LD framing and flattening algorithms. This adds processing overhead and requires heavy software libraries (like PyLD) which cannot be run in lightweight, browser-based, or static environments.

> ⚠️ **[REVIEW]** yes, so?  Why does RO-Crates require the flattened format?


*   **Archive Distribution Scaling:** Mapping deep folder paths inside a zip archive using `hasPart` containing MediaObjects does not scale well. For datasets containing thousands of individual component files, the manifest file itself can become larger than the actual data.

> ⚠️ **[REVIEW]** Good point.  the Crossaint approach using slug names for file patters is the solution, just haven't plugged it in yet.  (when there are thousands of component files, like the XCT data in astromat, the file names are patterned, so the slugs work)

---

## 3. Summary of Compliance Challenges

```mermaid
graph TD
    classDef barrier fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef solution fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    B1["CRS Coordinate Transformation <br>(Discovery)"]:::barrier
    B2["Bidirectional SKOS Hierarchies <br>(Codelist)"]:::barrier
    B3["Physical column to Variable Mapping <br>(Data Description)"]:::barrier
    B4["Flat vs. Nested Graph conversion <br>(Manifest)"]:::barrier

    S1["Automated GIS crosswalks"]:::solution
    S2["SKOS rewrite scripts (broader/narrower sync)"]:::solution
    S3["Header extraction & schema mapping tools"]:::solution
    S4["Server-side JSON-LD Framing pipelines"]:::solution

    B1 --> S1
    B2 --> S2
    B3 --> S3
    B4 --> S4
```

### Recommendations to Mitigate Compliance Barriers:
1.  **Automated Mapping Tooling:** Develop standard post-processing utilities (similar to `ddi_to_cdif.py` or `dcat_to_cdif.py` in the validation repository) to automate coordinate transformations, SKOS bidirectional additions, and CSV header extraction.
2.  **Middle-Tier Framing Services:** Use server-side framing pipelines (e.g. using `FrameAndValidate.py`) to shield metadata authors from structural nesting constraints, allowing them to author flat metadata that is framed automatically before schema validation.


---
### Source Document: PascalFeedback/compliance_challenges.md

# CDIF Profile Compliance & Implementation Challenges Report

This report analyzes the compliance requirements, required elements, and practical implementation barriers across the Cross-Domain Interoperability Framework (CDIF) profiles: **Core, Discovery, Data Description, Data Structure, Codelist, Provenance, and Manifest (Packaging)**.

---

## 1. Compliance Architecture Overview

CDIF enforces compliance using a two-stage validation workflow:
1.  **JSON Schema Validation:** Structural validation (closed-world) verifying that required properties, array structures, and JSON keys are correctly structured. This requires JSON-LD framing to shape the RDF graph into a normalized tree before validation.
2.  **SHACL (Shapes Constraint Language) Validation:** Semantic validation (open-world) checking cross-node constraints, vocabulary checks, and conditional logic directly on the RDF graph.

---

## 2. Profile-by-Profile Compliance Analysis

### A. Core Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/core/1.0`
*   **Core Required Elements:** `@id`, `@type` (must include `"Dataset"`), `schema:name` (meaningful title), `schema:identifier` (resolvable URI or `PropertyValue`), `schema:dateModified`, `schema:subjectOf` (CatalogRecord linkage), choice of rights (`license` or `conditionsOfAccess`), choice of download (`url` or `distribution`).

#### Practical Compliance Barriers & Challenges:
*   **Ambiguity in Metadata Provenance:** Separation of the metadata record itself from the resource it describes is achieved via a nested `dcat:CatalogRecord`. Legacy search indexing engines (like Google Dataset Search or standard catalogs) do not Monatively parse this nested structure and often conflate the catalog record's modification date (`schema:sdDatePublished`) with the dataset's modification date (`schema:dateModified`).

> ⚠️ **[REVIEW]** this approach solves the long standing ambiguity on what schema:dateModified actually qualifies. If a client doesn't parse the CatalogRecord, no information will be misinterpreted, but the update date for the metadata node would be lost. 


*   **Access Rights Structure:** Many repositories do not provide a machine-actionable license URI or formal access conditions, but instead provide long unstructured legal text blocks. Mapping these into a `LabeledLink` (`schema:CreativeWork`) requires manual curation or complex text extraction.

> ⚠️ **[REVIEW]**  If the repository only provides unstructured legal text, complex text extraction is going to be required, no matter where you put it in the JSON. In cdifCore this text would be inserted as text in the schema:conditionsOfAccess, not in a LabeledLink; the schema allows either option (or just an @id object reference to something).

---

### B. Discovery Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/discovery/1.0`
*   **Discovery Required/Conditional Elements:** `schema:variableMeasured` (required for datasets), `schema:spatialCoverage` (required if geographically bounded), `schema:temporalCoverage` (required if temporally bounded).

#### Practical Compliance Barriers & Challenges:
*   **Geographic Coordinate Standardisation:** Spatial bounds must be defined in decimal degrees using the WGS 84 datum. Most legacy spatial metadata records (e.g. from ISO 19115 or local GIS databases) store extents in custom UTM zones, local projections, or named projections (e.g. EPSG codes), requiring coordinate transformation pipelines to pass validation.

> ⚠️ **[REVIEW]** "Most legacy spatial metadata records..." -- what's the evidence?  all the ISO19115 profiles I've worked on require WGS84 decimal degrees-- this is a requirement for interoperability (like speaking the same language).  Yes the data provider has to do a SRS conversion, but if they're using any modern GIS system, that's a trivial operation; metadata harvesters on the other hand are generally not equipped with SRS transformation capabilities.


*   **Temporal Extents (OWL Time):** Geologic time, cyclicity, or named ordinal eras must be mapped using `time:ProperInterval`. Representing geological boundaries (e.g. "Jurassic") in a machine-readable format that crosswalks cleanly with calendar time is a massive semantic challenge.

> ⚠️ **[REVIEW]**  the whole point is to enable temporal systems based on named ordinal eras for time positions that predate any calendar, and might not have known numeric temporal positions.  There are ordinal eras that overlap with calendars (e.g. 'reign of Henry VIII).


*   **Variable List Extraction:** Extracting conceptual variables out of raw data distributions (such as CSV file headers) to populate `schema:variableMeasured` is highly labor-intensive and lacks standard vocabulary mapping, leaving them as plain strings that fail advanced semantic queries.

> ⚠️ **[REVIEW]** The perfect is the enemy of the good....  Extracting column headers from text based tabular formats files is generally pretty easy; yes, we might just end up with an instance variable that has a label, and yes, sometimes people create tables with headers that are nonsense, but in general between inspecting the content of the columns in the table, and the label string provided, we can provide useful, if not perfect information that will have an obvious path for improvement.

---

### C. Data Description Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/data_description/1.0`
*   **Data Description Required Elements:** `cdi:InstanceVariable` typing on variables, `cdif:physicalDataType` (array on variables, string on mappings), physical mapping (`cdif:hasPhysicalMapping` with `cdif:index` or `cdif:locator` and `cdif:formats_InstanceVariable` references).

#### Practical Compliance Barriers & Challenges:
*   **Physical Columns to Semantic Variables Mapping:** Physical column labels in raw files (e.g. `tmp_c_1`) must be explicitly mapped to semantic `InstanceVariable` definitions. If a dataset contains hundreds of abbreviated columns, creating these physical mapping nodes (`cdif:hasPhysicalMapping`) requires custom automated scripts.

> ⚠️ **[REVIEW]** I've not found this to be a problem that claude-code can't solve pretty quick.

*   **Value Domain Isolation:** CDIF requires separating substantive values from sentinel (missing/fill) codes (such as sensor `-9999` fill values or survey refusal codes) using `cdif:SubstantiveValueDomain` and `cdif:SentinelValueDomain`. Standard repository exports typically intermingle these inside data columns, requiring manual dataset inspection to extract and structure them.

> ⚠️ **[REVIEW]**  I agree-- this is an important point; we need a simpler way to represent value enumerations that include both sentinel and substantive values. See [value domains-- sentinel values should be indicated by a 'type'
 ](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/issues/1)

*   **Primary Key Modeling:** Multi-column keys require assembling `cdif:hasPrimaryKey` with ordered `cdi:ComponentPosition` nodes. Traditional repository metadata (such as Dataverse or Zenodo) does not export primary key constraints, necessitating custom post-processing to derive them.

> ⚠️ **[REVIEW]**  that is probably the case, but how often do we have to deal with multi-column keys. In the examples I've worked with so far, I havn't even found a primary key definition...  the IdentifierComponent usually fills the role. 

---

### D. Data Structure Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/data_structure/1.0`
*   **Data Structure Required Elements:** `cdi:isStructuredBy` pointing to `cdi:DataStructure` on distributions, subtyped layout classes (Wide, Long, Dimensional, Key-Value), and reusable represented variables (`cdi:RepresentedVariable`).

#### Practical Compliance Barriers & Challenges:
*   **Modeling Complexity for Long Layouts:** Long-format datasets (where variable names and values are stacked in rows) require matching `cdi:VariableDescriptorComponent` to `cdi:VariableValueComponent`. This is a highly abstract structural modeling paradigm that standard developers struggle to implement correctly.

> ⚠️ **[REVIEW]** I don't doubt it! Is there a better way?


*   **Deep JSON-LD Nesting:** By lifting value domains and units to `cdi:RepresentedVariable` and linking them via `cdif:uses`, the JSON-LD document becomes deeply nested and extremely difficult to inspect or author manually.

> ⚠️ **[REVIEW]** that's only required if one is creating a standAlone structure definition, and yes that reusability generates complexity. Fortunately, there shouldn't be much (if any) manual editing of this kind of metadata.

---

### E. Codelist Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/codelist/1.0`
*   **Codelist Required Elements:** `skos:ConceptScheme` defining the vocabulary, and `skos:Concept` defining terms. Must provide preferred labels and definitions.

#### Practical Compliance Barriers & Challenges:
*   **Strict Bidirectional Hierarchy:** CDIF mandates that all hierarchical relationships be defined in both directions: parent concepts must link to children via `skos:narrower`, and child concepts must link back via `skos:broader`. Standard vocabulary management systems (like PoolParty, VocBench, or Protégé) often export hierarchies unidirectionally, causing exported codelists to fail CDIF SHACL rules.

> ⚠️ **[REVIEW]** A topic for discussion.  In order to only use skos:broader, in JSON-LD the vocabulary has to be represented a graph, with a node for each concept.  To generate a JSON-compatible (hierarchical, nested) representation, you have to go from conceptScheme-->topConcept-->narrower-->other concept.   We were given the requirement that skos:broader relations are required if the vocab is hierarchical.  The ramification is that both broader and narrower are required.   Fortunately its a pretty easy sparql insert to get both relations in. 


*   **Handling Array Exceptions:** Because Codelists do not enforce strict array wrapping for repeatables (to comply with standard SKOS serialization), client parsing software must write custom conditional checks to handle both single string values and arrays.


> ⚠️ **[REVIEW]**  Interesting, I wasn't aware strict array wrapping for repeatables is standard SKOS serialization; the schema I looked at allow string or array values. In the other CDIF schema we do require  array wrapping for repeatables.  ?should we revise the schema?

---

### F. Provenance Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/provenance/1.0`
*   **Provenance Required Elements:** `prov:Activity` subtyped as `schema:Action`, `prov:used` (inputs), `prov:wasAssociatedWith` (performers), `prov:Entity` subtyped as `schema:Dataset`, and `prov:wasGeneratedBy`.

#### Practical Compliance Barriers & Challenges:
*   **Workflow Granularity Bloat:** Pipeline tools (such as Snakemake, Nextflow, or Galaxy) produce highly granular execution logs. Converting every command step into a `prov:Activity` linked by `prov:wasInformedBy` results in massive metadata files that can overwhelm search indexers.
*   **Actor Identification:** Automated processing runs are typically executed by system accounts, service workers, or virtual nodes rather than individuals. Mapping these to valid schema.org `Person` or `Organization` nodes with unique identifiers (like ROR or ORCID) is often impossible without inventing dummy records.

> ⚠️ **[REVIEW]**  noted. this prov profile is a draft, not part of the release packages.

---

### G. Manifest (Packaging) Profile
*   **Conformance Identifier:** `https://w3id.org/cdif/manifest/1.0`
*   **Manifest Required Elements:** Flat `@graph` structure in RO-Crate, metadata descriptor `ro-crate-metadata.json`, root dataset remapped to `"./"`.

#### Practical Compliance Barriers & Challenges:
*   **Translation Overhead:** Converting between nested trees (normal CDIF) and flat graphs (RO-Crate) requires running JSON-LD framing and flattening algorithms. This adds processing overhead and requires heavy software libraries (like PyLD) which cannot be run in lightweight, browser-based, or static environments.

> ⚠️ **[REVIEW]** yes, so?  Why does RO-Crates require the flattened format?


*   **Archive Distribution Scaling:** Mapping deep folder paths inside a zip archive using `hasPart` containing MediaObjects does not scale well. For datasets containing thousands of individual component files, the manifest file itself can become larger than the actual data.

> ⚠️ **[REVIEW]** Good point.  the Crossaint approach using slug names for file patters is the solution, just haven't plugged it in yet.  (when there are thousands of component files, like the XCT data in astromat, the file names are patterned, so the slugs work)

---

## 3. Summary of Compliance Challenges

```mermaid
graph TD
    classDef barrier fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef solution fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    B1["CRS Coordinate Transformation <br>(Discovery)"]:::barrier
    B2["Bidirectional SKOS Hierarchies <br>(Codelist)"]:::barrier
    B3["Physical column to Variable Mapping <br>(Data Description)"]:::barrier
    B4["Flat vs. Nested Graph conversion <br>(Manifest)"]:::barrier

    S1["Automated GIS crosswalks"]:::solution
    S2["SKOS rewrite scripts (broader/narrower sync)"]:::solution
    S3["Header extraction & schema mapping tools"]:::solution
    S4["Server-side JSON-LD Framing pipelines"]:::solution

    B1 --> S1
    B2 --> S2
    B3 --> S3
    B4 --> S4
```

### Recommendations to Mitigate Compliance Barriers:
1.  **Automated Mapping Tooling:** Develop standard post-processing utilities (similar to `ddi_to_cdif.py` or `dcat_to_cdif.py` in the validation repository) to automate coordinate transformations, SKOS bidirectional additions, and CSV header extraction.
2.  **Middle-Tier Framing Services:** Use server-side framing pipelines (e.g. using `FrameAndValidate.py`) to shield metadata authors from structural nesting constraints, allowing them to author flat metadata that is framed automatically before schema validation.


---
### Source Document: _static/footer.md

<hr style="margin-top: 3em;">

<div style="font-size: 0.85em; opacity: 0.85; margin-top: 1em;">

*We appreciate constructive feedback. Contact us at <cdif-feedback@codata.org> or file a [GitHub Issue](https://github.com/Cross-Domain-Interoperability-Framework/cdifbook/issues/new/choose).*

*Copyright (c) 2022-2026 Committee on Data of the International Science Council (CODATA). The Cross Domain Interoperability Framework (CDIF) is licenced under CC-BY-4.0.*

<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQECWAJYAAD/4QBoRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAARAAAATgAAAAAAAAJYAAAAAQAAAlgAAAABUGFpbnQuTkVUIDUuMS4xMgAA/+IB8ElDQ19QUk9GSUxFAAEBAAAB4AAAAAACAAAAbW50clJHQiBYWVogB9AAAQABAAAAAAAAYWNzcE1TRlQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPbWAAEAAAAA0y0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJd3RwdAAAAPAAAAAUclRSQwAAAQQAAAAOZ1RSQwAAARQAAAAOYlRSQwAAASQAAAAOclhZWgAAATQAAAAUZ1hZWgAAAUgAAAAUYlhZWgAAAVwAAAAUY3BydAAAAXAAAAAJZGVzYwAAAYAAAABgWFlaIAAAAAAAAPNRAAEAAAABFsxjdXJ2AAAAAAAAAAECMwAAY3VydgAAAAAAAAABAjMAAGN1cnYAAAAAAAAAAQIzAABYWVogAAAAAAAAnBgAAE+lAAAE/FhZWiAAAAAAAAA0jQAAoCwAAA+VWFlaIAAAAAAAACYxAAAQLwAAvpx0ZXh0AAAAAAAAAAAAAAAAZGVzYwAAAAAAAAAGb3BSR0IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/9sAQwALCAgKCAcLCgkKDQwLDREcEhEPDxEiGRoUHCkkKyooJCcnLTJANy0wPTAnJzhMOT1DRUhJSCs2T1VORlRAR0hF/9sAQwEMDQ0RDxEhEhIhRS4nLkVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVF/8AAEQgAXgHCAwESAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A9P1bVbfRrB7273+ShAOxcnk4HH41jfED/kUrn/rpF/6GK2oQU5qLM6knGN0Qf8LH0T0uv+/P/wBevLK7fqtPzMPazPU/+Fj6J6XX/fn/AOvXllH1Wn5h7WZ6n/wsfRPS6/78/wD168so+q0/MPazPU/+Fj6J6XX/AH5/+vXllH1Wn5h7WZ6n/wALH0T0uv8Avz/9evLKPqtPzD2sz1P/AIWPonpdf9+f/r15ZR9Vp+Ye1mep/wDCx9E9Lr/vz/8AXryyj6rT8w9rM9T/AOFj6J6XX/fn/wCvXllH1Wn5h7WZ6n/wsfRPS6/78/8A168so+q0/MPazPU/+Fj6J6XX/fn/AOvXllH1Wn5h7WZ6n/wsfRPS6/78/wD168so+q0/MPazPU/+Fj6J6XX/AH5/+vXllH1Wn5h7WZ6n/wALH0T0uv8Avz/9evLKPqtPzD2sz3DRtZtdcszdWfmeUHKfvF2nI/8A11g/Dj/kW3/6+H/kK469NU52ib05OUbs66isDQKQkDqcUALSbl9R+dAC0gIPQ5oAWigAooAKKACigAooAKTIHU0ALRQAUUAFFABSEgdTigBaKACkJA6nFAC0UAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQBzPxA/5FK5/wCukX/oYo+IH/IpXP8A10i/9DFdOF/ir5/kZVvg+78zyWivUOUKKACigAooAKsJYXL2ktysT+XGyqflOcnOMfl+tQ6kFJRb1Y7O1y9ougzaw7GN0Eaq27DjcDjjj0J71UstSutMMn2STyZJMBnA+bAOcc9vWuXFxxUklh5Jev8AXX0LpuC+NEN1ayWc7QTFPMT7wRwwB9MjvTZpTPPJKwUNIxYhRgZPJrpp8/Kufch2vodLDPoo8ONE9vF9sYG48jzWwzLwPm7EjnbmuXrjlgE6/t+eV+13a3bv+PyNPa+7y2RJBC1zOsSFFZzgb22jPpk0xW2urYDbSDg9D9a7pX5Xy7mS31NbV/D1xpMMMsrR7XjXdlxnf3AHcCql9qt5qaqt5IJSjlkO0Arnqox26cVx4WOLi39Ykmt9Py+RpN03bkRTqx9gufsf2ryZPL83yvunOcZ6eldftIc3JfXf5EWdrleirEFFABRQAUUAepfDj/kW3/6+H/kKPhx/yLb/APXw/wDIV5mL/iHTR+E66iuU2OR+I5I8ORkEg/aF6H2NHxI/5FyP/r4T+Rrqwn8QyrfCZeleALbUdKtLx9RvEaeJZCq7cAkZwOKTSvAhv9KtLr+2byLz4lk8tDwuRnA5rWdS0mue3yM4x0Xu/idNpunWvg/RrppLmaWBGMzvIMsBgDgAe1QaxY/2Z4CvbPznn8m1ZfMfq3ua51+8qpSdzV+5BtI2NM1S11exW8snZ4GJALKVOQcHg1h/D8j/AIRGH2kl/wDQzSrwVOfKh05OUbs1dJ1+w1vz/sMjv5BAfchXBOfXr0rlPhqc/wBrkdC6n/0Krr0o07W6k05uV7m4fHOhLay3DXbKkb+WVMbBmb2Hf61zvw4soJr3U7iWJXkjKohYZ2gls4/IVVWlTp2euoozlK512jeJdN14uthMTIgy0bqVbHrz1FclpESW/wAVb6KFQke1/lUYAyqE/rSqUoqmqkQjN87gzqdZ8V6VoUoivZz5pGfLjUsQPU46VyvhiGO/8favNeoryxNIYw4zgh9uceygfnTdKEIKctbgpylJqPQr+ItYtNY8R6Bc6dceZEXQNjIIPmLwR2qTxfa29t430h4EVHmeJpAoxkiQAH/PpW1Hl9lPl/rQzqX543/rU7fV9csNDgWXUJxGG+6oBLN9AK4bxC883xGjVbQXrQqvlWzuFVvlLdTx1yfwrCnQi4c8jSdRqXKjr9H8XaRrk/kWdwfOxkRyKVLfTPWuW1XT9d1PVrG+i0JbKe2cEtHcIS4BB56dOfzp+yptPWz9Uw55J9/kzs9X12w0OFZL+fZv4RFBZm+gFcZrcaX3xPsba8G+AKgCN0Pys38x+lKnRi6bqSCVRqagiHxp4l07XvD8R025JeO4y6EFWA2Nzj0q58TrO2j0y0uEjRJ/MMeVABK7ScfmBW2F5HN8qM6/Mo6naab/AMgu0/64p/6CKNN/5Bdp/wBcU/8AQRXDL4mdK2OO+KJYaXY7SQTM3Q/7Bo+KRI0uwI6iZv8A0A12YL4mYYj4Uaf/AAneg20iWr3bM6qFZo4yyg49RT9W0rT08ETxJDEsUVr5kbBRkMFyGz65rGKpSly2Zbc0r6GjqPiHTtLsYb24mY205ASSJC4ORkdPauT8P6e+t/Dq5s25ZZHMGezAhh+uRTdKEKnJN6ApylC63O4N7ALD7b5g+z+X5u//AGcZz+VeZ/8ACQk/Dn7Bk/aPN+y7cc7Pvfy+Wn9WfteTp+gvark5j0TSNZtNctmuLFnaJW2FnjK8/j9aZ4d0waRoVpaEDeqZkI7ueT+prGooKVobGkb29406KzKCigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigDmfiB/yKVz/wBdIv8A0MUfED/kUrn/AK6Rf+hiunC/xV8/yMq3wfd+Z5LRXqHKFFABRQAVPZWcl/cLbwyQpK/C+a20E+g96idSNOPNN2QJN6I2bTxVNa6P9g/esSjr5+/5kJ+7t9hVTXtFOj3hTzYmjbBjXfl8Y6kY4Gc15lKlgcZL6xBJv/Ly2N5Sq01yMysknJJJPUmivWMAooAKKACigAooA6A+Kpzov9nfvd3lbftHmfPuz/6Djj1qjoeknV75IRLEqggurNhyvcqMc15dehgsNJ4moknvf/gbG0ZVJrkTM2repae+mXj28ksTupORG27aO2eODjtXfSqwqx56bujKUXF2ZUorUQUUAFFAHqXw4/5Ft/8Ar4f+Qo+HH/Itv/18P/IV5mL/AIh00fhOuorlNjF8UaHJ4g0tbSKdYGEofcy7hwDxjPvW1VwnKDvEmUVJWZU0qzbTtKtLNnDtBEsZYDAbAxnFW6mTcndjSsrIr31nFqFjPaT58qdCjY64IqxQm07obV9GcRp/gvV7EPZprzR6a7EvHFHh2B64J+6T6iu3rV15vf8AJGapxWxzvhbww/h03oNwkqXDAoFUjYBnAPPPWuiqZ1JTtzFRio7HO+FfDUvh43hluUn+0MGG1Cu3Gff3roqJ1JTtzBGKjsc3beGJYPGVxrhukaOVSBCEORlVHXP+z6V0lDqycOToHIlLm6nJax4OuJ9ZOraLf/Ybt/8AWZXIJxjI+vcHIrraca04rlvoJ04t3OJfwJdzajZ39xqxuLqORZJ3kj+/tYEBQD8o4P5121P287NX0D2cdzm/EfhT+2LuG/sro2eoQYCygZBA6Z+nP510lTCrOCsmOUIy3OQtPCGoXGrQX+vaqbtrf/VpEuwevPtnnGOa6+m602rbIShFO5znibwoNclhu7W4+y30HCy4yCAcjOOeD0NdHShVnD4WOUFLc4a98C6nq1p/xM9bNxdg4jYx/Ii9+BjJPHNdzVqvNO60+SJdOLVmQ2sJt7SGEncY41Qkd8DFTVg3fU0Of8V+HJPEdtaxRXCQeTIXJZC24YxjqK6CtIVJU9YkyipbnEXXgnVZIhYQa6w0rIxBImWUemR1FdvVKvNa/oifZxM/T7Kz0DS4bVJFjhiGN8jAbmPJJPqTmn6rpNprVi1nfRl4WYMQGKnIORyKi6lK82VaytE8407TLXVPiHKtmRJYxTG4LAfKcYOB7bzXoek6Fp+iRumn24jL/fYkszemSea6J4hcnJAzjT97mkaNFchsFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQAUUAFFABRQBzPxA/5FK5/wCukX/oYo+IH/IpXP8A10i/9DFdOF/ir5/kZVvg+78zyWivUOUKKACigCS3nktbhJ4SBJGcqSM4PrUdTKKkuWSugTtqie6vbi98s3UplaMFVdvvYznBPeuhsrLSJPDkkknnLcSAyiLzF8xvLznZx0PNec8ZSo1vYxg1fey0v08tTb2cpR5mzl6CQSSBgdhnOK9MxCigAooAKKACigCa2u5rNne2kMbuhQuv3gD1we3SuiNlo/8AwjIkHnefj7V5Pmr5mPu+n3e/TNebLGU51/YSg38tL9u17GyptR5k/wDhjnLm5lu52mnbfKwG5sYLYGMn3qKvQjGMFyxVkYtt6sKKoAooAKKAPUvhx/yLb/8AXw/8hR8OP+Rbf/r4f+QrzMX/ABDpo/CddRXKbGT4j1xdA0prwwmZtwRUDYyT6n0rnviTp8T6bDqJZ/OhcRKuflwx5z78V04eEZytIyqycVdG1c6vcDwY+qxlFufsnnAAZVW256elYUGjwaZ8PL+eF5Ge9shLIHOQDt7e3NPkh7ZRXcHKXs2/I3PCWrz6r4fjvNQkj81pHUsAFGA2BXK+FfCltr/h4S6hPO0YkdYIkfCx88nHck56068Kanq7eiFTlJx7no4IIyDkGvP/AAFqMtppesRyu0kVj+8RSemA2QPQfLWdWi4NJO9yoVOZM79pEQgO6rnpk4zXkemvomsG5vPFepuLuRv3abj8ox1HB4zwB7Vo8Ny/E38lclVb7Hr1cJ8PdWeW4v8ASzdG6gt/ngkJyduSPy6HHbNZ1aLp2fRlQqKWh3R6UHoawNDzjTPEHi3Wp7mPTntX8g/NvQLgEnH8qzPC/wDb32u//wCEf8jdked52OmWxjP416VSEYpWS+ZyRbbd7/I6m1/4Tn7XD9pFl5HmL5m3bnbnnH4ZqXTP+Ez/ALSt/wC0vsf2Pd+92Y3Ywen44rCWkX8JrHfqdYWAOCRmuD8V/wDI+6Hz/wA8/wD0M1nCjzwc77FynaSXc7wkDqQPrXEfFEkaHaYOP9IP/oDUUKXtZWvYVSpyK525YAckCuA+ILbfDWjt6OD/AOQzRSo+0k432CdTkSZ329d+3cN3XGea5HSvDUOjr/wkN1czXN8ts0su/GCSueOM8dKmUIrRO7GpPqtDrnkSMZd1XPqcV5v4e0D/AITT7TqmuXM0g8zYkaNgA4B49AM4AH41pKjGnpOWpKm5fCj0kEEZByK8/wBAlufDfjJtAa4eeymH7sOc7fl3Aj06EGplRtDni7oaqe9yvRnoG4ZIyMj3rzGHTn1fx/q1l9plggdmabymwzqNvy57ZJFV7BKCm3uL2l5OKR6ajpICUZWA9DmvNdSsP+EG8SafLpcsgtbk4eJmzkbgCD68HI9DQqCnFyg72B1HFpSR6WSFBLEADua838W6jFqHixdM1G8a10q3x5u3PzErnn8wPbmlToOUed7feEqlnyo9HV1cZRgw9Qc15VHqGl+H/Edg/hvUGls52CXEJY4GSB369cj6e9U8M3Fyj07qwva2aTPVmYKMsQB6k1x3jCwsLnULaXWtaFtYqv8Ax59C/qRg/TnFZ06amrt/hcuUmjsEkSQZR1Yf7JzXlGny6fY+MNOPh2W4W0ldUcSAgPkkHr1H9a0lh/dck9u6sQqmqTPWMjOMjPpXnfi6Oabx9p0NvM0EskaIsi9UyWBI98ZqYUeeDne1ipVLSUbHoYkQuUDqWHUZ5rzDxhoEHhX7FqGlyzrO0hDO8hZiwGQc/hyKqnQjU0jLX0FKo4ayR6jTImLwo56soNcpqcv4716+0GxtZdPdFeSRlbem7gLms34qf8gux/66v/6Aa7MJCMpNSVzCvJxirHcWzmS2iduWZAT9cUln/wAeVv8A9c1/lXI9zc5bwr4h1DVtf1S0vHjaG2LeWFTBGHI5PfgVl+A/+Rs1z6v/AOjWrsxEIxpxaX9WOelJuUk/63PQtw55HHXmvMtO01tX8baxZvcSxWzO7TCJtpkAbhc9hk/pWboKMFNvctTbk4pHpiOkgJRlbHoc15tb2K+GPiJZ2OnSSLbTgFkLZyGDcH15XNDoJ03Uiw9p73K0dfdvro8S262wh/sggebu27885x3/ALtc3rJP/C1NM5/gT+UlOEL0XLT7vQTlaoonfkgDJOBXn+vSXHiXxmugLcPDZQj94EON3y7iffqAM1EaN4c8nZFOp73KtWd+kiSDKOrAehzXm/iHQf8AhCja6podxMg8zY8btkE4J59QcEEH8KqNGNTSEtROo4/Ej0kkDqQPrXnvxBujc2GiXUPytJmRR6EhSKmlR9o2r2sOc+VJnoJkQOELqGPQE81514r8J2+naIdV+03E2oK6GSaR8lyxAOPTGeMU4UoTfKpa+gpTcVdrQ9HrK8NXUt74b0+4ncvK8KlmPUn1rGcXCTi+hpF8yTRq0VIwooAKKACigDmfiB/yKVz/ANdIv/QxR8QP+RSuf+ukX/oYrpwv8VfP8jKt8H3fmeS0V6hyhRQAUUAFFAB3zRQBteHtCXWZXzcRgIp3R5IcHHynp0zWXBeXFqrrbzPFvILFDgnHTmuLF0sRUSVCfL3/AK/M0pygviVwu7f7JcvB50czIcM0Wdue45qOWV55XlkOXclmOMZJ6mummpKK53d9SHa+gCNjbG4A/cq4jL9gxGcfkK6SLxPGmhGyZc3ZjJ8/yl2h/wCEEdzjvXHLEYlV+RUvd736/de3y+ZpyQ5L82pztvEs86RtKkIY43yZ2j64piuyyLID8ysGBPrnNd0k3FpOzMlubeu+Hxo8UDtcxZeMApk7ncfeI46dKyp766uk23M8kwDlxvOcE9cen06Vx4WliYN+3nzX7L8PTsaTlB/CrFfvnvS13GYUUAFFABRQAUUAepfDj/kW3/6+H/kKPhx/yLb/APXw/wDIV5mL/iHTR+E66iuU2Oc8cadc6n4ceKziMsqSJJsXqQDziujrSnUdOXMiZxUlZnE2Umqah4Jv9Pn0qaCSC0EMOQczHaRwDjHQfnXbVTq++ppai5Pd5WznfA9lc2HhuKC8geCYSSEo45ALEiuiqalR1JczHGKirI4bwZot3Adai1C1lgjuvlUuMbgS+cfnXc1VSs528hRgo38zznSk1jwibiyl0RtShZ90U0Yzk4x6Hg4HB6V6NVSr8/xq4lT5dmc/4WXWXhmuNaiggLn91EkYV1H+0R+GB7V0FZznzdLFRjbqIehpazKPL9DXxH4dubx7bQpZ/tBGd/GACcYx9a9QrpliOZJSinb1MlSs7pnFxeJPFTzRrJ4b2ozAM2TwM8mu0qHUj/Kvx/zKUX/N+RxPjbStRfVdO1bTrdrj7NjcickENuHHp1HFdtRTrOCcbXTCUFJpnnHihdf8T6ZEy6NJbxRPlYid0jsQRnHGFHv616PVQr+zd4xRMqfMrNnEeONKvtQ8O6bBZ2ks8sZG9EHK/uyOfxrt6mlWdOTkkVOCmrMrLbibTRbzA7Xh2OPqMGrNZX1uWed6YniDwXJcWkemNqNnI+5HjJ69M8AkZAGRivRK3lX5/jSZmqfL8LscT4d0XU77xFJ4g1qEW74PkwHqOMD6AD88121TOtKUeVaIcYJO/U8uik1CD4g6rcaXAtxNEzs0LNjzE+XIB9eh/Cuu07wxJY+Kr3WGuldLkMBEEIK5K9889PSt5VoexjHd9jJQftGzn5LPWPGHiGznvtOewsbQ5/edTyCRz1JIA6YAr0OsvbtRcYK1zT2abu3c4fxFo+o2PiaLXtMtBeoQBNAMZzjB49CMdOhFdxUwrOMeRq6G4Jvm6nGWV5r2r6zCYtJj03Tkx5v2iIFm9cdDnt6d67Oh1FayigUXe7ZwGvafqFj40XWBpr6lalQAiDdtwMYx2IPI7c139ONZqHI1dCcLy5jzu+t9b1HxLpeqS6PLDbRuoWNSGaNQ3JbHTrnHtXolNV7RcUlZg6d2m2cXrmmX1x4/0u8htZXtYgm+UD5VwW6/mK7SpjWcYOFtxuCclLscd8RdMvdT0y0jsLWS4dJWLLGM4G0iuxoo1nSd0E4KasyOAFbeMEYIUAj8KkrEs57xnoMuv6OIrbb9ohfzEVjgNwQRn6GuhrSnUlTd4kyipKzPPrXxD4rsrJLJ9CklmjXYszI3bgEgcH869Bq3Vi3dwRPI1pc5DwN4evNLF3fakuy5uyP3ZIJAySScdyT0rr6mpWlUtccYKOxxfh3TL228a6vdT2skdvLv8uRh8rZYHiu0pzquUFB9AUEm2cVq+l303xF069itZHtI1QPMB8q43/4iu1ojWcabp23E6acuY4rVdLvpviNp99HaytaRogeYD5VwH/xFdrRGs1TdO243BOXMcR4h0XVLDxJH4g0WEXDEDzYR1Jxg/UEY6cgiu3ohWlGPI9UJ003fZnneox6/41mt7SXTX02yjbc7yE9cYzyBngnAxXolUq/J8CSB0+b4nc4nxzo91c2+kw6daSzpbkqQgztGABn8q7app1nTvbqOUFKxz/jOzuL7wvPBaQvNMzRkIg5OGBNdBU06jpy5kOUVJWZk+F7ea08NafBcRtFNHEFdG6qa1qmcnOTk+o4rlVkFFSMKKACigAooA5j4gkDwjcknA8yL/wBDFdMyhhhgCPQitaVT2cuaxE480bHz95if3l/Ovf8AyYv+eaf98iur64v5fxMfYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPueAeYn95fzr3/yYv8Anmn/AHyKPri/l/EPYPucp8NyD4acg5/0h/5CusVVUYVQB7CuWtU9pLmsbQjyqw6isiwooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigAooAKKACigD//Z" alt="Funded by the EU">

*CDIF v.1 was supported by the EU Horizon Europe funded WorldFAIR project (GA 10105839). CDIF v.1.1 is is a community effort coordinated by CODATA. Further development will be supported by the EU Horizon Europe funded CDIF4EOSC project (GA 101292473).*

</div>


---
### Source Document: background/checklistForImplementation.md

# Checklist to Implement

## Scenario: Metadata Publisher

The user represents a community that is generating data or other information resources, and making those resources accesible online.  The user needs to make those resources discoverable, with information in the metadata so that the search client can do at least a superficial evaluation of a discovered resource, and the search client can obtain the resource in a useful format, following any designated security or privacy protocols.

1. Review the CDIF content model requirements.  Is the necessary information available about the resources you offer?  Choose the level of documentation required to enable data access (are there security/privacy concerns), and data integration. For data integration, is the goal machine-actionable data integration, or simply to enable discovery based on the information provided by the resource?

2. Determine how to generate CDIF JSON-LD metadata records from your internal data system that contains metadata about your community's offerings. Use the [JSON_LD implementation information](../metadata/schemaOrgImplementationpatterns.md) and [examples](../examples/index.md) in the CDIF GitHub for guidance.  The assumption is that this metadata is already in some kind of structured information system e.g. a spreadsheet, relational database, or triple store.  If the listing of offerings is in text documents, you will need to figure out how to get these into a format that can be machine processed. If there are only a few resources for which you want to publish metadata, manually constructing the needed JSON-LD metadata documents might very well be the simplest approach. 

3. Make the metadata records accessible on the web.   There are two common paths here. 
	1. Create a web-accessible folder that contains a collection of metadata documents you want search engines to harvest and index. Each metadata document must be accessible via URL. 
	1. Embed the JSON-LD as \<script\> html elements in landing pages for the resources you want indexed. In some situations, landing pages are generated via scripts from a database backend or internal metadata file format; in these cases this second approach is generally more straight forward, by adding the necessary code to this process to generate the CDIF JSON-LD script.   The choice of which approach to use will also depend on the capabilities of the metadata aggregators that you want to harvest your metadata. In some cases, you might need to implement one of the open-source catalog software platforms, e.g. Geonetwork-Opensource, Geoportal, CKAN, Deegree...., that implements a standard harvesting protocol. This can get significantly more complicated.

4. Generate a sitemap and get it on your website. This is a simple xml file that contains a list of URLs, with other optional properties like a 'last modified date', in a standard format that most web scraping applications can use. A Robots.txt file in the root of the website where you are publishing the metadata contains a link that points to the sitemap. The sitemap.xml and robots.txt files are widely used and understood by metadata aggregators. 

5. With all this in place, its a good idea to notify any metadata aggregators you want to harvest your metadata to make sure they check you sitemap.  Don't be surprised if there are bugs found in the pipeline between your internal metadata information system and the harvester's index.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: background/conformance.md

# Conformance with the CDIF Guidelines

CDIF is not a standard - rather, it is a recommended use of existing standards to support a greater degree of interoperability across domain and infrastructure boundaries. Thus, it is different from most technical standards: it does not establish new models of formats for metadata, but indicates how specific existing ones can be implemented to become more interoperable. There are two different levels of conformance, one requiring more strict adherence to technical implementation guidelines than the other. These are described as "forms of conformance."

There different forms of conformance with the CDIF Guidelines are: (1) conformance at the content level, and (2) conformance at the implementation level. The difference is that while content conformance guarantees that the needed set of core information to support a FAIR function is present, it makes no guarantees regarding how that information is formatted or implemented. Thus, the use of the information may require processing or transformation to be interoperable at a machine level. While desirable, this is a lesser form of interoperability than implementation conformance. When implementations are conformant, direct machine-to-machine interoperability is possible without further processing or transformation being required. 
These two levels of conformance can be expressed as *contracts*:

## Content Conformance

*The metadata instance in question satisfies all the requirements of the CDIF profile at the level of its conceptual model. All information that is required is provided, according to the requirements of the profile, even though it may be expressed in syntaxes which are not recommended by the guidelines. A mapping between the recommended implementation and the one provided must be possible, and should be provided. The existence of content conformance is asserted in documentation, but is not necessarily indicated in any machine-readable fashion.*

## Implementation Conformance

*The metadata instance in question satisfies all the requirements of the CDIF profile implementation, such that it validates against the models expressed in both the SHACL rules and the JSON Schema, and with any other specified constraints in the associated documentation.*

Implementation conformance requires and builds on content conformance, because the implementations are based on the conceptual models for each profile. Ideally, every FAIR implementation exposing or consuming resources across domain or infrastructure boundaries would be implementation conformant, but that seems unlikely in the near term. CDIF hopes to promote both alignment of metadata content as well as implementation by providing a path for gradual adoption where appropriate. 

The intention of the CDIF profiles is to have as small a set of required metadata as possible to support any given function, but to also have an agreed set of useful metadata which is optional but has a common expression when it is included. The existence of additional metadata is always allowed - CDIF describes a core set of information, not a closed, proscriptive one.

In order to inform metadata consumers about the profile(s) that a given metadata record conforms to at the Implementation conformance level, identifiers are assigned to each conformance class. These are resovable http URIs. By default, the identifier resolves to a web page describing the profile for humans. Using content negotiation or adding a file extension, the URI can be used get the JSON schema or SHACL rules to validate the instance.  These identifier a supplied in a CatalogRecord object for the metadata record, using the dcterms:conformsTo property.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: background/development.md

# Development, Production, Dissemination, and Maintenance 


## Background

The goal of this section is to provide a brief overview of how the Cross-Domain Interoperability Framework (CDIF) will be developed, produced, disseminated, and maintained into the future, starting with Version 1.1.  The first version of the guidelines was produced as an output of the WorldFAIR project, and has undergone further development and maintenance under the WorldFAIR+ initiative, leading to the new release, Version 1.1. It is expected that several ongoing projects such as CDIF4XAS, CLIMATE-ADAPT4EOSC, and especially CDIF4EOSC will drive significant further developments. Consequently, an attempt is made to establish a stable framework within which these developments can be managed.

CDIF has identified many different aspects of FAIR-supporting systems in cross-domain scenarios which will benefit from agreements about the metadata to be exchanged. These are termed "FAIR functions," and include such things as cataloguing, search, and discovery; description of data sets; description of access to and licensing of resources; description of data provenance; data packaging; data transformations and mappings; description of controlled vocabularies and code lists; and so on. The list is a long one. 

In each of these areas there are existing standards, and typically more than one, with many being domain-specific and not used or useful outside their intended domain scope. CDIF identifies agreed standards - and agreed, limited implementation of those standards - so that the core information needed to support any particular FAIR function will always be understood by the counterparties involved. Thus, it is a growing lingua franca for use of FAIR resources across domains and infrastructures which otherwise would not use the same standards. 

CDIF has taken a pragmatic approach, prioritizing what it sees as the most important functions, and those which can most readily be adopted: profiles have been created for discovery, data description, code lists, and basic access, along with conventions in the important areas termed "universals": time, geography, and units of measure. For each, a set of recommendations has been made. To summarize these, a set of core metadata fields has been identified, along with a mechanism for their expression and publication on the Web. Metadata is expressed in the form of JSON-LD, a syntax which is commonly used on the Web, but which marries developer familiarity with the richness of RDF.

This paper briefly describes the processes for development, production, dissemination, and maintenance of CDIF. Several new profiles will be added to Version 1.1, and a much large number in subsequent releases. Each new function is supported in its own "profile," a set of technical and documentary resources which enable developers to implement interoperable sets of metadata for each specific function. These profiles are the items which are developed and produced for use.

The development, production, and maintenance processes are coordinated by the CDIF Editorial Team, drawing on the expertise of other members of the CDIF WG. (Note that this document does not address the governance or organization of CDIF.)

Use the CDIF.org website to find the latest information regarding what profiles are currently available, which are under development, and which are planned. This is also where information regarding the CDIF Working Group and CDIF Advisory Group may be found.

## Development of CDIF Profiles

CDIF is developed by teams of experts who are typically volunteers or project participants with an interest in the existence of CDIF because of the interoperability it will enable. Research is increasingly data-intensive and cross-domain in orientation, making the need for something like CDIF increasingly urgent. Many volunteers are involved with the development of other technical standards and specifications in areas related to FAIR use of resources. 

These individuals are brought together by CODATA as the coordinating body, providing the expertise and work force for the development of CDIF. They are organized into two groups: the CDIF Working Group and the CDIF Advisory Group. The Working Group performs most of the development, with the Advisory Group in a steering and review capacity.

When a new profile has been identified for development, a series of meetings are held, going through several steps:
1. Landscape review: Identification of the current state of play, scope, and requirements.
2. Narrative: Creation of a description of the purpose of the profile - how it will be used, what problems it will solve, and what business functions it will support.
3. Conceptual model: A syntax-independent modelling of the information needed for the profile, bearing in mind existing system capabilities and information holdings.
4. Implementations and examples: The use of one (or, if needed, more than one) common standard(s) for the implementation of the identified information, and creation of syntax examples based on real use cases. This both tests earlier steps and illustrates the solution to be recommended.
5. Hand-off to production: This stage involves working with the production team to make sure that the profile is formally modelled as intended in UML, and that the outputs created contain the needed information. Input in the form of specific documentation is critical so that the intention of the developers is communicated to end users effectively. 

### Development platform
Github will be the development platform, using the [https://github.com/Cross-Domain-Interoperability-Framework](https://github.com/Cross-Domain-Interoperability-Framework) organization.  There are separate repositories for each profile. 

Development work should be organized in the main branch of a repository. Work should generally start by creating an issue describing planned contribution, and then creating a branch with the issue number in the branch name.  When the contribution is ready, create a pull request to merge the branch into the main branch. When the pull request is merged, the issue can be closed, and the branch deleted (it will still be in the GitHub history). If a contributor does not have permission to create a branch in the repository, they should create a fork to host their work.  

### Identifiers for CDIF resources

URIs will be resolved using the w3id redirect service ([https://github.com/perma-id/w3id.org#permanent-identifiers-for-the-web](https://github.com/perma-id/w3id.org#permanent-identifiers-for-the-web)).  Many of these will redirect to released in GithHub. Artifacts that are not managed via github can be published on cdif.codata.org with w3id redirects to those locations.   New releases will require updating the .htaccess files at [https://github.com/perma-id/w3id.org/tree/master/cdif](https://github.com/perma-id/w3id.org/tree/master/cdif). 



## Production of CDIF Profiles

For the existing CDIF profiles, all of the various artefacts (documentation, SHACL validation, JSON Schemas, examples) have been created by hand. Up until now, ythere has not been a consistent set of artefacts for the profiles, but an evolving one. A standard set of artefacts has been identified as a result of several different projects and implementations, so that there will be a consistent in version 1.1 and beyond. This will include:
1. High-level documentation describing the purpose of the profile, and describing the Conceptual Model as a set of information requirements
2. Field-level documentation for each recommended syntax implementation, provided in the form of a normative document.
3. SHACL for validating the profile
4. JSON Schema for validating the profile
5. JSON-LD examples
6. JSON-LD Framing for the profile
7. Clickable Field-Level documentation, linking all of the syntax artefacts (SHACL, JSON Schema, etc.) together with detailed documentation for developers
8. A UML formalization of the profile implementation, expressed as Canonical XMI, and according to the UCMIS style to ensure interoperability across UML tools
9. *Potential/Future:* Pydantic classes to enable easier Python implementation
10. *Potential/Future:* OGC Building Blocks to enable easier domain-level adaptation and specification

The production flow in future will start with the creation of the UML model for each profile implementation, working with the development team on the basis of the Conceptual Model and the syntax implementation and examples. Once the production team has developed a suitable UML model, this will be used to drive the coordinated generation of all of the other artefacts.

It is worth describing why the UML: model is used in this way. It is often the case that UML is employed to define a conceptual formalization. That is not the case here. RDF vocabularies are often modelled in a fashion which does not fit neatly into the object-oriented style of UML formalizations, so the more generic style used in the RDF community is employed here (essentially, "boxes and arrows" based on the RDF information model, as often seen in W3C Recommendations). The CDIF Conceptual Model for each profile is documented, but is not formalized as a UML model during initial development. 

The UML formalization is not a single implementation model, but a somewhat generalized one, as it must span implementation in a set of different syntax-bound outputs: SHACL, JSON Schema, OO classes like Pydantic, etc. All of these artefacts must be coordinated, or the profiles will not function as intended. (E.g., a JSON-LD metadata instance must be valid according to both the JSON Schema and the SHACL rules, etc.)

Given the number of profiles anticipated, as shown in the diagram below, it is essential that the artefacts themselves are generated from a single source of truth, so that they remain consistent without the risk of manual error.
  
While the UML model for each profile may be useful to implementers, and will be made available to them in an XMI format for reuse, it is primarily a part of the CDIF production system, and should be considered as such. It is not itself a deliverable for direct use, unlike other artefacts (such as SHACL rules, JSON Schema, Pydantic classes, etc.)

![CDIF Profiles - current and planned](CDIF_Profiles_Future.jpg)

## Dissemination, Maintenance, and Versioning of CDIF Profiles

Once all the different artefacts for a profile have been produced, and have gone through the approval process, they will be published in the CDIF Book as part of a versioned release. Each profile implementation will have a version assigned to it, indicating the current version. This mechanism will be used to track minor changes, such as documentation edits,  and additions (as for new types of artefacts), but will not be indicative of major changes to the recommendations themselves. Major changes will be part of larger, numbered  releases (as we see from Version 1.0 to Version 1.1). 

All of the CDIF artefacts are stored in the appropriate GitHub repositories. In the case of explanatory text, this may be in the form of the Markdown which is used to populate the CDIF Book. Other non-narrative forms of documentation (field-level documentation, JSON Schemas and examples, SHACL rules, etc.) will be managed in a related production repositories, which will also serve as the basis for the technical distributions.

GitHub issues and pull requests will be used as the basis for a regular process of reporting bugs and requesting features in existing profiles using standard GitHub workflows. The CDIF Editorial Team is responsible for performing this maintenance on a technical level.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: background/history.md

# How was CDIF Developed?

The idea for CDIF came initially from a series of workshops held at Schloss Dagstuhl in Wadern, Germany,
starting in 2018. The focus was on the alignment of standards from different domains, and the events were
co-hosted by the Data Documentation Initiative (DDI) Alliance, building on a long-running series of Dagstuhl
events. Each year subsequently, [further discussions were held](https://codata.org/initiatives/decadal-programme2/dagstuhl-workshops/).

Participants in the workshops included standards developers and implementers from a wide range of
backgrounds, and a general effort was made to keep the work grounded by including participants from a
range of scientific domains, as well as computer scientists and standards and infrastructure experts. While
sometimes exploratory or theoretical, use cases from the real world were used as a basis for the work.

As the subject of how standards could be used together was explored further, it became clear that
substantial interoperability across domain boundaries would be possible if some basic agreements could be
forged on the content and expression of key metadata.

These discussions provided input to the planning for CODATA’s ‘Making Data Work for Cross-Domain Grand Challenges’ programme (Sponsored by the International Science Council, as part of the [ISC’s Action Plan](https://council.science/actionplan/) ), in which the ideas for a standards-based interoperability framework became more fully formalised, in line with the recommendations from the EU’s [‘Turning FAIR into Reality’ report](https://data.europa.eu/doi/10.2777/1524). While similar work such as the EOSC Interoperability Framework was ongoing, none of this work specifically addressed the field-level alignments across metadata standards which could produce machine-to-machine interoperability in a cross-domain scenario.

With the WorldFAIR project, it became possible to access a range of domain expertise around FAIR, and to ground the work on CDIF more broadly. Each of the WorldFAIR Case Studies completed an initial FAIR Implementation Profile, and this served as input to provide an overview of what standards were currently in use and which were being considered. The FIPs also provided a view into the degree of standards adoption across different communities. Subsequent meetings were held with each group to look at how well the domain-neutral standards being considered for inclusion in CDIF served to describe FAIR data and resources from those communities. These inputs proved to be valuable. To cite two examples:

- In Work Package 07 on Population Health, Schema.org was used extensively to describe the context of an experiment for the purposes of exchange, in line with work done by the Observational Health Data Sciences and Informatics (OHDSI) group (which provided the Observational Medical Outcomes Partnership (OMOP) Common Data Model used as a standard data description in that community). As in many other examples, the implementation of Schema.org relied on JSON-LD.
- The Work Package 11 Oceans Science and Sustainable Development Case Study provided a view of the way a large-scale knowledge graph could be developed on the basis of a common core of metadata fields, again using Schema.org embedded in landing pages as JSON-LD. More information on WP11’s relation to CDIF is available in [WorldFAIR D11.2](https://zenodo.org/records/7682399)

Synergies such as these emerged from the work, and helped to guide the development of the CDIF recommendations. Other connections to the Case Studies may be less evident, because the CDIF functionality is truly broad in scope, and attempts to provide a solution for all domains, and not just those represented in the project. This is reflected in the use of standards and technologies which are seen as widely used across all domains. The issues being addressed by CDIF apply to all domains, and so may not derive directly from specific statements reflected in any individual Case Study.

The work on CDIF was primarily conducted by a group of 30 invited experts, divided into a Working Group and an Advisory Group. Representatives from many different FAIR initiatives, implementations and standards bodies were included, many of them having attended the Dagstuhl workshops in preceding years. The Working Group met every two weeks over the duration of the project, discussing and drafting specific recommendations which were then passed to the Advisory Group for review. Public review of initial drafts was also informally conducted in some cases.

An effort was made to consider additional successful examples in related fields. While there is no existing cross-domain network for FAIR data today, there are initiatives from the scientific world and the world of official statistics which proved valuable in showing which approaches could be employed. Among these was the [Statistical Data and Metadata eXchange (SDMX) Initiative](https://sdmx.org/), which provides a standards-based framework for the exchange of statistical data and metadata among national and international statistical agencies and central banks in a broad global network. Significantly, SDMX standards are employed in the collection and publication of the [Sustainable Development Goals (SDG) Indicators](https://unstats.un.org/sdgs/indicators/indicators-list/). The Helmholtz Metadata Collaboration (HMC) likewise served as an example of how a large number of disparate research centres in Germany could exchange data and metadata in a practical fashion, leveraging the ODIS approach. Several such examples were considered, with an eye toward identifying practical implementation approaches.

The criteria for selecting standards for cross-domain use include:
1. they should be domain-agnostic — that is, not based on assumptions specific to a particular domain;
2. they must be open;
3. they should be already in use for the intended purpose, to the greatest extent possible;
4. they should be adoptable — that is, there is a community which can support them, provide tools and knowledge, etc.; 
5. they should support anticipated functions in the future, at least to a reasonable extent.

These criteria limit the number of candidates to a relatively narrow field, as much of the work on standardisation has been grounded in specific domains. Specifications intended for use on the Web are prominent, as these frequently meet the criteria given above.

CDIF has been developed with a knowledge that there cannot be, and likely never will be, a single set of standards useful for all FAIR exchanges in all situations and across all domains. It is clear that a much higher degree of convergence is possible. Within domains, standards-based approaches have proven to be successful in many different areas. CDIF attempts to start an ongoing process defining what such a convergence can look like, based in approaches shown to work, and using standards and technologies fit for the purposes of cross-domain exchange.

---
### Source Document: background/principles.md

# Design Principles

## Overview
The Cross Domain Interoperability Framework is based on a set of concrete, implementation-level principles intended to enhance any community’s data management approaches and reduce the barriers to reusing data across domains. These principles will guide the selection of CDIF recommended standards and approaches intended to inform project-level planning and to provide practitioners with clarity regarding the work involved and the skills, personnel, and technology required. The guidance offered by these principles should not be read as absolute requirements; they define aspirations that should be pursued as far as feasible. In the discussion that follows we will use the term ‘data’ for any structured information representation that is intended for use by computer information systems. This includes both direct observational or model data and data describing other data, commonly differentiated as metadata, but subject to the same principles.

## List of Principles
In this section, we set out the principles that have guided the development of the CDIF to date.

### Pragmatism
CDIF is not just a set of theoretical standards and guidelines, but a recommended approach that can realistically be implemented, taking into account the capabilities and limitations of (meta)data producers and consumers. This implies considering the known time limitations, resources, and technical capabilities of those expected to implement it. The framework must balance between flexibility and rigid requirements, providing helpful guidance and a systematic approach, with room for adaptation to new situations and requirements, but within clearly defined bounds to preserve interoperability.

(mainstream)=
### Mainstream
Technology and standards recommended by CDIF should build on existing systems and the legacy investment of (meta)data providers and consumers. User familiarity with recommended implementations is desirable, and these should be widely recognised and in line with current production systems. There will always be new standards and technology, and CDIF will need to keep pace with these on an implementation level, but the goal should always be to employ existing technology, rather than to try to anticipate what practice will be in the future. Use existing Web architecture51 whenever possible. For example:
- HTTP methods (POST, GET, PUT, PATCH, and DELETE) to operate on resources;
- Resource-oriented, API-driven architecture to support file-based download as well as interactive, query-driven access;
- Ensure identifiers are dereferenceable over the Web using the HTTP(s) protocol;
- Alternate serialisations can be requested using content negotiation or signposting links.

### Atomicity
Manage data at the finest granularity possible. Information is organised into entities that have sets of properties, and each property has a value that is an instance of another entity, or a simple value that is a number or a category (represented by a word). In practice, this can lead to complex, nested data schemas that are difficult to understand, manage and use, so it is necessary to consider the requirements of the application for which the information will be used, and the trade-off between the cost of complexity and the benefits of granularity. Information captured in free text is useful for human reading, and natural language processing is getting better at extracting structured data from text, but it is subject to semantic fuzziness and misinterpretation. The benefit of highly granular, or ‘atomic’ data is composability: it can be disaggregated and reaggregated to accommodate diverse and evolving standards, and support projection into different forms in an integration-on-demand model.

### Data as an asset that is worth investment
View data as an asset that has value outside of its immediate application. In practice, this is implemented by making data and associated documentation (metadata) persistently available on the Web, with identifiers at all levels of granularity that can be dereferenced using standard Web architecture, and representation formats using one or more prevailing domain-specific or domain-neutral standards. Identifiers in the data should provide linkage to other resources on the Web.

The goal is to enable automation of the data-discovery-to-use workflow to the maximum extent possible. CDIF is intended for data producers who put data on the Web with the intention that it be used. The approach is to generate machine-actionable (atomic) documentation that is as expressive as possible, e.g., very precise and clear definitions, complete descriptions, and links to supplementary metadata. CDIF can be understood as recommendations for implementation of the FAIR Data Principles, extending them to address more concrete issues.

Documentation for data should be targeted to future users, human or automated, who are temporally or socially removed from your current community. Background knowledge and assumptions that are currently obvious might not be obvious to those users. The terminology used should be clearly defined in plain language, and the definitions should be updated as needed such that they will be accessible and current for the lifetime of the data.

### Flexibility and tooling to encourage uptake
Create and share the ability to project data and its metadata into serialisation formats that are useful for a variety of data consumers across domains. Offering data content in multiple human languages supports different language-based communities. From a machine-processing point of view, multimodality will usually entail:
- Creation, documentation, exposure, and maintenance of authoritative mappings between syntactic and semantic conventions within and between domains;
- Development of software that leverages these mappings to automate the presentation of data in forms familiar to end users or to developers.

Standards used to interchange data should be as domain-agnostic as possible, with mapping files and documentation, which must qualify any loss of precision where it occurs. In practice, this means that categorical properties should usually be represented using key-value approaches, with conventions for vocabularies specifying both property types, and vocabularies specifying the range of values associated with each property.

### Broadcast system capabilities
The Web is too big for all users to keep up with who does what, who holds what data, and how to access the data. Data providers have to be proactive by presenting a machine-actionable description of their interoperable data offerings and services, defining the datasets offered, service protocols used, vocabularies, access policies, or any other digital resource. The CDIF needs to define conventions for publishing server capabilities.

### Robustness
Trust in data quality and the longevity and reliability of systems in a cross-domain digital ecosystem is critical to user engagement. Maintaining this robustness has a technology aspect and a business aspect. The architecture and implementation of systems in a cross-domain digital ecosystem should support the addition, update, or retirement of their components. This entails avoiding dependence on any single component, whether it be hardware, software, standards, or conventions. A component-abstraction layer in the architecture can enable of-the-moment components to be swapped. Focus on maintaining basic cross-domain interoperability functions using proven off-the-shelf components. Functionality can be extended, but beware of becoming a silo through dependence on bespoke tooling or approaches.

Robustness from a business point of view is in many ways a bigger challenge. We can point at some
necessary factors, but these are not always sufficient. Systems must define their market niche, making sure
that there is a value proposition that is clear to the system stakeholders so they ‘buy in’ and continually
support the system. Effort to increase awareness of the system capabilities — marketing, training, workshops
— is likely to be necessary. Avoid building cross-domain technology ‘just because’: make sure someone
clearly benefits from the technology, and they know about the technology.

### Show and tell
Collect and publish metadata related to the use of CDIF to show what implementers have done and what the results of those investments have been. A living, visible system will generate trust and uptake; and ensure that the CDIF remains fit for purpose as technology and priorities evolve. A framework that is not used will not continue to function. Make it easy to determine what standards are used, where data are shared, how data can be accessed, who is reusing data, and what the effects are of data reuse. This kind of information will also facilitate changes to improve the framework and its implementation.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: background/structure.md

# The Structure of CDIF

The organisation of the CDIF recommendations follows a basic functional breakdown emerging from the need to support certain exchanges of information as dictated by the FAIR Principles. ‘Findable’ requires that we be able to make our resources searchable, and enable them to be catalogued. ‘Accessible’ requires that we can retrieve or link to resources in a technical sense, but also that we can understand what conditions are in the case that access is limited. ‘Interoperable’ means that we can load resources into our systems for processing once acquired, and operate on them in a meaningful way. ‘Reusable’ means that we have enough information to understand the data and the uses to which it can legally be put.

There is not a point-for-point alignment between the FAIR Principles and the functional requirements that support them. The information needed to support one principle may be required also to support another, and there may be no clear distinction made between these sets of information. CDIF organises FAIR ‘functions’ in a fashion that maps to the principles, but more between systems needed for implementation and the information they require:

- Discovery, Cataloguing, and Dissemination (F)
- Controlling Data Access (A)
- Data Description, Use, and Integration: Structure and Semantics (F, A, I, R)
- Characterizing Data/Provenance and Process, Quality (I, R)
- Universals: Time, Geography, and Units of Measure (F, I, R)

This organisation is not strictly functional, but attempts to describe the information needed for each major function (Discovery, Access, Integration, Reuse) as well as to address some of the common information needs (concept schemes, codelists, and mappings, "universals"). Not all topics are covered in equal depth at this time: some are supported more thoroughly in this version of the guidelines than the others, which will receive more attention in future. This reflects the current state of play within the FAIR community, and the perceived relative importance of these functions based on current and planned implementations.

These areas were identified through examination of FAIR implementations in many domains, and are driven by the relative maturity of the standards and practice within communities engaging proactively with FAIR. Discovery is perhaps the most common subject of FAIR implementation, as it is both less demanding in terms of metadata (and therefore resources) as well as being logically a first step: if you can’t find it, you can’t use it! Access to open data is in some senses a 'solved' problem, so the attention of the FAIR community is turning towards the need to better support access to controlled data. Currently, support for providing access to controlled data is often strictly manual, presenting a practical bottleneck for reuse. 

While we are early in our development of standards and systems for automating access to controlled data, there are some initial steps which can be easily taken. Data interoperability and reuse have been receiving an increasing amount of attention in many domains: these are arguably the most metadata-intensive aspects of FAIR, but they also hold a huge potential in terms of efficiency gains: if we can ease the problems of integration and harmonisation ('data wrangling') through automation, the potential resource savings are large. Data integration necessarily raises the question of how semantics are exposed and mapped. These topics provide the focus of the current document and the CDIF profiles.

# Summary of CDIF Profiles and Recommendations

**General**: CDIF metadata should be embedded in landing pages or linked stand-alone files, encoded in JSON-LD. The supported profiles will be indicated as part of the metadata.

[**Core Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/metadata/core/): The Core profile identifies a set of fields from [Schema.org](https://schema.org) for use in all other profiles, covering such basic functions as management of the metadata and statements of conformance.

[**Discovery Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/metadata/discovery/): This profile recommends the use of a set of key [Schema.org](https://schema.org) fields for describing static datasets and queryable data sources, with the [DCAT](https://www.w3.org/TR/vocab-dcat-3/) equivalent recognised as an acceptable alternative.

[**Manifest Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/manifest/manifest/): This profile is used to describe packages of metadata and FAIR resources, to form bundles for dissemination, archiving, etc. It can be used to render “webby” FDOs. The recommended implementation uses RO Crate.

[**Access Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/data-access/intro/): This profile recommends that [ODRL](https://www.w3.org/TR/odrl-model/) Actions and Entities be used to describe policies and conditions for the use of data. At this time, the utility of this approach is limited by the lack of shared vocabularies for conditions of use, user qualifications, legal constraints, and similar important items. ODRL is thus limited to describing policies in terms of the disseminating institution, but provides a basis for expansion in future when the needed vocabularies are developed.

[**Concept Scheme Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/controlled-vocabularies/conceptprofile/): This profile recommends the use of [SKOS](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) for describing controlled vocabularies, understood to mean any terminological resource. The use of [OWL](https://www.w3.org/TR/owl2-overview/) as a linked extension towhat is presented in SKOS is also recommended, as is the use of [XKOS](https://ddialliance.org/Specification/RDF/XKOS) for formal statistical classifications.

[**Data Description Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/data-description/datadescriptionprofile/): This profile recommends the use of [Schema.org](https://schema.org) and [DDI-CDI](https://ddialliance.org/Specification/ddi-cdi) to provide a granular description of quantitative data sets, and how the logical content of those datasets relates to their physical encoding. Both text-based (i.e., CSV, fixed-width) and binary (i.e., NetCDF, HDF5, Parquet) are supported. The recommendations cover description of individual data sets to make them ‘integration-ready’.

[**Codelist Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/controlled-vocabularies/codelistprofile/): This profile recommends the use of [SKOS](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) for describing the enumerated sets of values used to populate the fields in data sets. These are used in the description of data sets and their structures in the Data Description and Data Structure profiles.

[**Data Structure Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/data-description/datastructureprofile/): This profile uses [DDI-CDI](https://ddialliance.org/Specification/ddi-cdi) to describe reusable data structures and variables. In future, this capaility will be extended to data formats.

[**Universals Profile**](https://cross-domain-interoperability-framework.github.io/cdifbook/universals/univintro/): This section recommends the information which should be provided when describingtime, geography, and units of measurement in other metadata sets. Some standards for this purpose arerecommended in each area.


The CDIF includes recommendation for specific implementation approaches in each profile, based on web technology. While many standards and vocabularies require the use of RDF, it is not a technology that is commonly used in every domain. The solution to this is to advocate the use of JSON-LD, which allows the expression of RDF vocabularies in the common JSON syntax.

In each profile a minimum set of required fields are specified to support common cases. Other optional fields are suggested, and the path forward toward support of more complex scenarios is indicated. While FAIR implementation is demanding, it is hoped that consistent use of a common core of metadata can minimize the effort required.

Users only need adopt those profiles that are useful to them. There is no requirement for the adoption of optional profile content. For example, it is possible to describe data to make it ‘integration ready’ at a detailed level, but not to support profiles for data discovery or access, to give but one example. CDIF profiles are intended to be a toolkit for implementation, with the needed functions being addressed in any specific setting according to implementer priorities.

For some common combinations of profiles, implementation artefacts will also be provided as a convenience.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: background/whycdif.md

# Why CDIF Matters

CDIF is designed to address the question of what standards should be used, and how should they be implemented, which arises almost immediately in the implementation of systems in accordance with the [FAIR Data Principles (Wilkinson et al., 2016)](https://doi.org/10.1038/sdata.2016.18). The FAIR principles require that data and metadata be described according to common standards and made available through common protocols and mechanisms, but as principles, they do not specify which standards and protocols. Within the context of a specific domain or infrastructure, established practice can provide some guidance, and implementers use the standards and protocols that are common within that domain or infrastructure. 

In a scenario where FAIR resources are intended for use across domain and infrastructure boundaries this approach breaks down. It requires systems in every domain to support the standards and protocols of every other domain whose resources might be of interest. Given the number of different functions that need to be supported for the discovery, access, integration, and use of data, and the number of standards and protocols these functions require, this becomes an overwhelming task. CDIF attempts to provide recommendations to help resolve this issue with a set of non-domain-specific standards and their implementation for scenarios where FAIR exchanges are taking place across domain and infrastructure boundaries. While there is no authority that can dictate how the FAIR principles are to be implemented, it is possible to recommend a single approach to promote convergence on a set of standards, at least for typical cases. While adoption of such recommendations is of necessity voluntary, the utility of a common approach will serve as the motivator.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: controlled_vocabularies/codelistprofile.md

# Codelist Profile

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelistProfileStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelistImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/rules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelist-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/tree/reviewRevision202606/Examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCodelist/index.html)

A CDIF codelist is a controlled vocabulary or classification scheme represented as a [SKOS](https://www.w3.org/TR/skos-reference/) `ConceptScheme` serialized in JSON-LD. The profile composes the base SKOS ConceptScheme and Concept building blocks with CDIF-specific constraints: resolvable identifiers, required definitions, bidirectional hierarchy, and the mandatory CDIF Core metadata properties. It aligns with the approach described in ['Modelling of Eurostat's Statistical Classifications in ShowVoc'](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc).

All property names use namespace prefixes declared in the `@context`:

```json
"@context": {
  "skos": "http://www.w3.org/2004/02/skos/core#",
  "schema": "http://schema.org/",
  "dcterms": "http://purl.org/dc/terms/"
}
```

Additional prefixes may be added for concept URIs (e.g. `"sf": "https://w3id.org/isample/vocabulary/sampledfeature/"`).

[Graphical presentation of Codelist profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCodelist/index.html)

## Codelist concept scheme

The root object representing the controlled vocabulary or classification scheme, typed as `skos:ConceptScheme`. It carries the scheme-level properties below together with the mandatory CDIF Core metadata.

### \@id
- **Cardinality:** mandatory
- **JSON:** `"@id": "{URI}"`
- **Description:** Globally unique, resolvable URI for the concept scheme.

### \@type
- **Cardinality:** mandatory
- **JSON:** `"@type": ["skos:ConceptScheme"]`
- **Description:** Must include `skos:ConceptScheme`.

### skos:prefLabel
- **Cardinality:** mandatory
- **JSON:** `"skos:prefLabel": "Sampled Feature Type vocabulary"` or an array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** Preferred human-readable label for the scheme. At most one per language.

### skos:hasTopConcept
- **Cardinality:** 1..*
- **JSON:**
  ```json
  "skos:hasTopConcept": [
    {	"@id": "id for concept node", 
		"@type": ["skos:Concept"], 
		"skos:prefLabel": "{{string}}",
        "skos:notation": "{{code string for concept}}",
        "skos:inScheme": [
			{"@id": "{{id of this ConceptScheme}}"}
	},
	{.. possibly other codelist concept instances}
  ]
  ```
- **Description:** Top-level concepts that have no `skos:broader` within this scheme. The JSON-LD hierarchy is rooted here — all child concepts are reached by traversing `skos:narrower` from these top concepts. Items may be inline concept objects or [object reference](#object-reference)s.

### schema:identifier
- **Cardinality:** mandatory
- **JSON:** `"schema:identifier": "https://w3id.org/isample/vocabulary/sampledfeature/"` or a [PropertyValue](#sec-propertyvalue-id)
- **Description:** Primary identifier for the codelist (a CDIF Core metadata property). Takes precedence over `dcterms:identifier`.

### schema:dateModified
- **Cardinality:** mandatory
- **JSON:** `"schema:dateModified": "2024-04-19"`
- **Description:** Date (ISO 8601) when the codelist was last modified. Takes precedence over `dcterms:modified`.

### schema:license / schema:conditionsOfAccess
- **Cardinality:** mandatory — at least one
- **JSON:** `"schema:license": [{"@id": "https://creativecommons.org/licenses/by/4.0/legalcode"}]` or `"schema:conditionsOfAccess": ["{text}"]`
- **Description:** A license (URI or [object reference](#object-reference)) or a text statement of access conditions; at least one is required. `schema:license` takes precedence over `dcterms:license`.

### Optional scheme properties
- **Cardinality:** optional
- **JSON -- Description:**
  - `schema:url` -- web page describing the codelist.
  - `schema:creator` -- Person, Organization, or `@list` of agents (author/maintainer); `dcterms:created` — original creation date.
  - `schema:version` -- version identifier for the scheme.
  - `skos:definition` -- formal explanation of the scheme's meaning or purpose.
  - `skos:altLabel`, `skos:hiddenLabel` -- alternative and search-only labels.
  - Documentation notes: `skos:note`.

(codelist-concept)=
## Codelist concept
A `skos:Concept` with CDIF constraints, representing a single term or category within the scheme.

### \@id
- **Cardinality:** mandatory
- **JSON:** `"@id": "{URI}"`
- **Description:** Globally unique, resolvable URI for this concept.

### \@type
- **Cardinality:** mandatory
- **JSON:** `"@type": ["skos:Concept"]`
- **Description:** Must include `skos:Concept`.

### skos:prefLabel
- **Cardinality:** mandatory
- **JSON:** `"skos:prefLabel": "Natural Solid Material"` or an array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** Preferred label that identifies the codelist item for human users. At most one per language (enforced by SHACL `sh:uniqueLang`).

### skos:inScheme
- **Cardinality:** mandatory
- **JSON:** `"skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"}`
- **Description:** The concept scheme(s) this concept belongs to, each given as an [object reference](#object-reference).

### skos:definition
- **Cardinality:** optional
- **JSON:** `"skos:definition": "A naturally occurring solid material."`
- **Description:** Formal definition of this concept.

### skos:broader
- **Cardinality:** required if the concept is a value of `skos:narrower` on another concept
- **JSON:** `"skos:broader": [{"@id": "sf:anysampledfeature"}]`
- **Description:** Broader (parent) concept(s), given as [object reference](#object-reference)s. See [Bidirectional hierarchy](#bidirectional-hierarchy). Top concepts must **not** declare `skos:broader` within the scheme.

### skos:narrower
- **Cardinality:** optional, repeatable
- **JSON:** array of inline [Codelist concept](#codelist-concept) objects or [object reference](#object-reference)s
- **Description:** Narrower (child) concepts. Each inline child must declare `skos:broader` pointing back to this concept. Use inline objects to build the JSON tree, or `{"@id": "..."}` references.

### skos:notation
- **Cardinality:** mandatory
- **JSON:** `"skos:notation": ["{{string}}"]`
- **Description:** Classification code(s) that identify the item for use in datasets / computer consumption. Should be unique within the scheme.

## Data types

This profile uses the shared [LanguageTaggedValue](#languagetaggedvalue), [object reference](#object-reference), and [PropertyValue](#sec-propertyvalue-id) patterns defined on the [Common data types](../metadata/datatypes.md) page.

(bidirectional-hierarchy)=
## Bidirectional hierarchy
CDIF codelists require concept hierarchies to be expressed in **both** directions:

- **`skos:narrower`** is needed because the JSON-LD tree is rooted at `skos:hasTopConcept`; without it, child concepts cannot be reached by traversing the document from the root.
- **`skos:broader`** is needed for upward navigation and for display trees in vocabulary browsers and classification tools.

Any concept that appears as a value of `skos:narrower` **must** also declare `skos:broader` pointing back to its parent. Top concepts (those in `skos:hasTopConcept`) must **not** have `skos:broader` within the scheme.

```json
{
  "@id": "sf:anysampledfeature",
  "@type": ["skos:Concept"],
  "skos:prefLabel": "Any sampled feature",
  "skos:definition": "Top concept",
  "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
  "skos:narrower": [
    {
      "@id": "sf:earthmaterial",
      "@type": ["skos:Concept"],
      "skos:prefLabel": "Natural Solid Material",
      "skos:definition": "A naturally occurring solid material.",
      "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
      "skos:broader": [{"@id": "sf:anysampledfeature"}]
    }
  ]
}
```

## Array convention
Unlike other CDIF profiles, the Codelist profile does **not** require repeatable properties to always be serialized as arrays. This follows standard SKOS practice, which allows either a single string or an array for literal values. Both of these are valid:

```json
"skos:prefLabel": "Material"
```

```json
"skos:prefLabel": [
  {"@value": "Material", "@language": "en"},
  {"@value": "Matériau", "@language": "fr"}
]
```

Consumers of CDIF codelist documents should test whether a value is a string or an array before iterating.

## Validation
- **JSON Schema** validates structure: required scheme properties (`@id`, `skos:prefLabel`, `skos:hasTopConcept`, `schema:identifier`, `schema:dateModified`, and license/access), concept requirements (`@id`, `skos:inScheme`, `skos:definition`), and bidirectional hierarchy (inline narrower concepts must have `skos:broader`).
- **SHACL** validates RDF constraints: `sh:uniqueLang` on `skos:prefLabel`, `sh:class skos:ConceptScheme` on `skos:inScheme`, `sh:class skos:Concept` on `skos:broader`, and the `narrowerImpliesBroader` rule.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: controlled_vocabularies/conceptprofile.md

# Concept Scheme Profile

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/cdifConceptSchemeStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/CDIFConceptSchemeImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/conceptSchemeRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/cdifConceptScheme-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/cdifConceptScheme/index.html)

A CDIF Concept Scheme is a controlled vocabulary or terminology represented as a [SKOS](https://www.w3.org/TR/skos-reference/) `ConceptScheme` in JSON-LD. It uses the same SKOS building blocks as the [Codelist](codelistprofile.md) profile, but `skos:Concept` has broader usage here: a concept can represent a possible value for a categorical variable, or an entity or property in a data model. Where the Codelist profile expects a simple, often flat list of coded values, the Concept Scheme profile accommodates richer terminologies with definitions, sources, and hierarchy.  

All property names use namespace prefixes declared in the `@context`:

```json
"@context": {
  "skos": "http://www.w3.org/2004/02/skos/core#",
  "schema": "http://schema.org/",
  "dcterms": "http://purl.org/dc/terms/"
}
```

[Graphical presentation of Concept Scheme Profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/cdifConceptScheme/index.html)

## skos:ConceptScheme

The root object representing the concept scheme, typed as `skos:ConceptScheme`. It carries the scheme-level descriptive properties together with the mandatory CDIF Core metadata (see the [Codelist](codelistprofile.md) profile for the full required-property set).

### \@id
- **Cardinality:** mandatory
- **JSON:** `"@id": "{URI}"`
- **Description:** Globally unique, resolvable URI for the concept scheme.

### \@type
- **Cardinality:** mandatory
- **JSON:** `"@type": ["skos:ConceptScheme"]`
- **Description:** Must include `skos:ConceptScheme`.

### skos:prefLabel
- **Cardinality:** mandatory
- **JSON:** `"skos:prefLabel": "{string}"` or an array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** Preferred human-readable label that identifies the scheme. At most one per language.

### skos:definition
- **Cardinality:** mandatory
- **JSON:** `"skos:definition": "{string}"`
- **Description:** An unambiguous statement of the meaning or purpose of the scheme.

### dcterms:source
- **Cardinality:** mandatory
- **JSON:** `"dcterms:source": "{string or URI}"`
- **Description:** The authority for the origin of the scheme's definitions.

(sec-skosconcept)=
## skos:Concept

A `skos:Concept` within the scheme. In the Concept Scheme profile a concept may represent a possible value for a categorical variable, or an entity or property in a data model. `skos:prefLabel`, a `skos:definition`, and a source citation are required; `skos:notation` is optional and used identically to the Codelist profile. The requirements for each concept in the RDF implementation:

### \@type
- **Cardinality:** mandatory
- **JSON:** `"@type": ["skos:Concept"]`
- **Description:** Must include `skos:Concept`.

### schema:identifier
- **Cardinality:** mandatory
- **JSON:** `"@id": "{URI}"` or `"schema:identifier": "{string}"` (see [PropertyValue](#sec-propertyvalue-id))
- **Description:** Each concept must have a globally unique, resolvable identifier.

### skos:inScheme
- **Cardinality:** mandatory
- **JSON:** `"skos:inScheme": {"@id": "{scheme URI}"}`
- **Description:** [Object reference](#object-reference) to the containing `skos:ConceptScheme`.

### skos:prefLabel
- **Cardinality:** mandatory, repeatable
- **JSON:** `"skos:prefLabel": "{string}"` or an array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** At least one preferred label; multiples are allowed but only one per language-locale (SKOS does not permit more than one `skos:prefLabel` per language).

### skos:definition
- **Cardinality:** mandatory
- **JSON:** `"skos:definition": "{string}"` or [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** A definition of the concept, also in language-specific form.

### skos:broader / skos:narrower
- **Cardinality:** required for hierarchy (see Description)
- **JSON:** `"skos:broader": [{"@id": "{parent URI}"}]`
- **Description:** If the scheme is hierarchical, use `skos:broader` to indicate a concept's parent. `skos:narrower` (the inverse) can also be provided, supporting navigation both up and down the hierarchy. See [Bidirectional hierarchy](#bidirectional-hierarchy).

### skos:notation
- **Cardinality:** optional
- **JSON:** `"skos:notation": ["{code}"]`
- **Description:** A code or abbreviation, unique within the scope of the vocabulary, that denotes the concept in data instances. Not required if unique URIs are used instead; the convention must be defined in a vocabulary profile. Notation values are commonly short strings that are easier to interpret than the concept identifier.

### skos:altLabel
- **Cardinality:** optional
- **JSON:** `"skos:altLabel": "{string or LanguageTaggedValue}"`
- **Description:** Other labels, also in language-specific form.

## Data types

This profile uses the shared [LanguageTaggedValue](#languagetaggedvalue), [object reference](#object-reference), and [PropertyValue](#sec-propertyvalue-id) patterns defined on the [Common data types](../metadata/datatypes.md) page.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: controlled_vocabularies/vocabintro.md

# Controlled Vocabularies: Codelists and Concept Schemes 

Terminology-based semantic resources are a key element in information systems, establishing the binding between the symbols (strings) manipulated by computers and human-intelligible meaning of properties, types, values, or any other element in a volume of data. These are a critical component in scenarios involving (but not limited to) data integration and harmonisation.

For the purposes of this document, we use the term ‘controlled vocabularies’ to cover all of the related set of terminology-based semantic resources, even though this may not be technically exact (ontologies, for instance, are often seen as a different kind of resource). Here, our use of the term potentially includes codelists, classifications, thesaurus, taxonomies, glossaries, ontologies, etc. In places where we specifically mean ontologies, classifications, or other types, these terms are explicitly used.
 
We envision two primary scenarios for FAIR usage of controlled vocabularies. In the first scenario (data-centric) an agent (human or machine) encounters a term, code, or symbol in a data set and needs to understand the meaning of that symbol, or to determine if its meaning is the same as some other term, code, or symbol. The navigation is from the individual symbol (code, term) to its meaning within the system of which it is part. 
In the second scenario a vocabulary as a whole is published as a reusable resource for use outside the context of a particular field in a data set. Navigation is from the vocabulary resource into a component part(term).

Both scenarios require description of the ability to navigate between the controlled vocabulary as a managed whole and its component parts.

To meet these use cases, each member of the vocabulary must have its own globally, unique, web-resovable identifier. These unique identifiers are used by machines to detect when the same concept is being used in two different data sets. 

Persistent, resolvable identifiers (PIDs) are required, with a globally unique mapping from the identifier to a concept. The identifier must be be resolvable on the Web to obtain a useful representation. How these identifier strings are formulated will vary widely across user communities. CDIF only recommends that they be included in the definition of a controlled vocabulary.
The goal is that identified concepts can be reused to ease the burden of data harmonisation: if two data sets use the same concept, by referencing the same PID, then there is no ambiguity. 

CDIF is recommending profiles for two kinds of controlled vocabulary resources: Codelists and Concept Schemes. A Codelist is a resource that maps short strings (codes) to meaning. At the simplest level meaning can be conveyed by another longer string--a 'label' that is more informative for users. Concept schemes are collections of information objects that represent concepts with a human-intelligible label, a definition that specifies the concept, and auxiliary information typically including relationships between concepts and information about the source of the definition. Codelists are intended for use in constructing user interfaces with pick lists for populating fields in datasets. Concept schemes are more broadly applicable to any situation in which the meaning of some information entity, e.g. class, property, property value, needs to be made clear to avoid misunderstanding in the interpretation of data.  Requirements for the Codelist and Concept Scheme profile are as follows.

### Codelist Requirements

- A codelist object must be documented with the required CDIF core properties: Identifier, Title, Date, License or conditions for use, a URL at which the codelist is accessible, and an identifier for the CDIF profile used to represent the codelist
- Every item in the codelist must have a unique 'code' that is used to represent the code in data instance
- Every item in the codelist must have a human-intelligible label
- Optional: identifiers can be assigned to codelist items; if no identifier is assigned, item identifiers will be assumed to be concatenation of the codelist identifeir, '/' and the unique code assigned to the codelist item. 
- Optional: a definition with a more complete explanation of what the code means.
- Optional: hierarchical links between items encoding 'broader' and 'narrower' relationships between items. Broader,narrower can be interpreted broadly according to the semantics of the codelist entries. To facilitate software applications using the codelist, broader and narrower relations must both be explicit in the codelist representation. 

### Concept Scheme Requirements

- A Concept Scheme object must be documented with the required CDIF core properties: Identifier, Title, Date, License or conditions for use, a URL at which the concept scheme is accessible, and an identifier for the CDIF profile used to represent the concept scheme.
- The concept scheme must identify the most general concepts in the scheme. If there is some hierarchy in the concept scheme, this will be a subset of the concepts; if the scheme is 'flat', then all concepts in the scheme will be listed.
- every item in the scheme must have a globally unique identifier
- every item in the scheme must have a human-intelligible label.
- every item in the scheme must have a text definition that unambiguously defines the meaning of the concept and differentiates it from other concepts in the scheme.
- every item in the scheme must cite the authority for its definition; the authority may be 'this scheme' if definitions are original to the concept scheme.
- Optional: hierarchical links between items encoding 'broader' and 'narrower' relationships between items. Broader,narrower can be interpreted broadly according to the semantics of the concept entries. To facilitate software applications using the concept scheme, broader and narrower relations must both be explicit in the concept representation. 

# Implementation

CDIF recommends the use of the Simple Knowledge Organisation System (SKOS) for representing concept vocabularies.  SKOS is a RDF vocabulary that includes predicates to assign an identifier to a concept,  provide a definition, and assign preferred, language-localized labels (strings) for human use to identify the concept. A vocabulary service exposing the SKOS content on the web is necesary to make the identifiers resolvable. 

This use of SKOS materially aligns with that described in the document [‘Modelling of Eurostat’s Statistical
Classifications in ShowVoc’](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc) for classification items.

CDIF recommends following the guidance provided by [Cox et al. (2021) ‘Ten Simple Rules for making a Vocabulary FAIR’](https://doi.org/10.1371/journal.pcbi.1009041). The CDIF recommendation to use SKOS (as described in this section) aligns with Rule 6 (Cox et al., 2021) regarding machine-readable formats for CVs.

## Note on formal statistical classifications
Documentation of formal statistical classifications includes additional information, but a detailed profile for CDIF has not been developed. CDIF recommends using the style used at [Eurostat](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc) and [FAO](https://www.fao.org/statistics/caliper/resources/data-modeling/en). These descriptions include additonal properties, and can include tables documenting mapping between versions of classifications. This information is represented using XKOS, see the [XKOS specification](https://rdf-vocabulary.ddialliance.org/xkos.html) and [user guide](https://linked-statistics.github.io/xkos/xkos-best-practices.html).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: controlled_vocabularies/xcdifskosprofile.md

# CDIF SKOS profile

A **skos:ConceptScheme**: a set of concepts that define the possible values for a categorical variable. The scheme can define a hierarchy of values from general to more specific. This hierarchy is represented using the skos:broader relationship linking more specific concepts to subsuming more general concepts. If a hierarchy is defined in the scheme the top concept(s), i.e. those that do not have any skos:broader associations, must be identified using the skos:hasTopConcept property on the skos:ConceptScheme.

**skos:Concept**: represent the possible values for a categorical variable. In the RDF implementation of a skos:ConceptScheme, these are the requirements for each concept:
- must specify rdf:type skos:Concept.
- must have a globally unique, resolvable identifier.
- must have a skos:inScheme relationship to the containing skos:ConceptScheme.
- must have at least one skos:prefLabel, but may have multiples as these are language specific (SKOS does not permit more than one skos:prefLabel per language-locale).
- must provide a definition of the concept with skos:definition, also in language-specific form.
- must use the skos:broader relationship to indicate its parent in the hierarchy if the concept scheme is hierarchical 
- a unique (in the scope of the vocabulary) skos:Notation must be provided if skos:Notation is used to denote the skos:Concept in data instances. This is not necessary if unique URIs are used instead of a skos:Notation in data instances. The convention must be defined in a vocabulary profile. skos:Notation values are commonly short strings or abbreviations that are easier for users to interpret than the concept identifier.
- Other labels may be provided using skos:altLabel, also in language-specific form.
- skos:narrower relationships (inverse of skos:broader) can be provided, supporting navigation both up and down the concept hierarchy.


This use of SKOS materially aligns with that described in the document [‘Modelling of Eurostat’s Statistical
Classifications in ShowVoc’](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc) for classification items.

---
### Source Document: controlled_vocabularies/xstatisticalclassification.md

# Statistical Classification

*tbd-- need definition of statistical classification, some detail about added xkos properties, perhaps some examples.*

Documentation of formal statistical classifications includes additional information. CDIF recommends the style used at [Eurostat](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc) and [FAO](https://www.fao.org/statistics/caliper/resources/data-modeling/en). These descriptions include additonal properties, and can include tables documenting mapping between versions of classifications. This information is represented using XKOS, see the [XKOS specification](https://rdf-vocabulary.ddialliance.org/xkos.html) and [user guide](https://linked-statistics.github.io/xkos/xkos-best-practices.html).

---
### Source Document: data_access/intro.md

# Data Access Recommendations

This section of the framework makes recommendations for describing and documenting policies related to the retrieval of a digital object for research, and subsequent operations performed on that digital object. In the CDIF framework, we use the term 'access' to include the activities connected to the initial retrieval of a digital object, and 'usage' to include all subsequent operations performed on that digital object.  Access and usage policies (herein 'access policies'), when defined, are typically unstructured and bespoke. Data providers may not make access policies explicit and when they do, they tend to re-invent new policies locally. Therefore data users experience new data access policy content and structure at every access-related interaction across the science system. Any kind of aggregation or orchestration of data across providers is stymied by an incoherent data access policy environment in terms of existence, coverage, content, and machine-actionability.

## Objective
The objective of the Data Access Profile in the Cross Domain Interoperability Framework (CDIF) is to progress to a more structured and standardised, machine-actionable approach. The benefits and convenience for data requestors accrue through:
- transparency and efficiency in requesting data;
- consistency of access experience across data custodians;
- automated processes and services across those providers;
- federated permissions query and access.

For data custodians, the structured and standardised approach to data asset permissions through a structured ontology (e.g., ODRL) provides:
- Default minimum good practice guidance and design patterns for new systems development;
- Efficiencies, equity, and transparency in processing access requests;
- Ability to track and evaluate access requests to improve processes and address inequities in access and reuse;
- Opportunities for repository or archive providers to participate in multi-organisational collaborations to support collaborative science.

The goal is interoperable, machine-actionable, expression of data access policies. It is important to note this is not the entirety of 'Access' from a plain English or FAIR perspective. Accessing sensitive data is a complicated, multi-faceted, multi-party process involving for example:
- Clarifying intellectual property rights, and, where appropriate, copyright.
- Negotiation with data producers
- Specifying data reuse licences
- Establishing bespoke legal agreements
- Ensuring cybersecurity
- Assessing data sensitivity and identifying potential secondary disclosure risks
- Preventing reverse engineering of the data
- Establishing the ethical and legal constraints pertaining to the nature of the data in question
- Clarifying the nature of a specific access, including the requestor and the data request purpose
- Identifying roles or attributes upon which access may be granted
- Provision of secure access environments with or without analytics
This recommendation acknowledges the importance of all those (and related) elements but focuses on standard ways of capturing data access requests in structured, machine-actionable policy statements at the point of access, as well as prescribing what subsequent operations can (or cannot) be performed until the end of the research lifecycle. CDIF does not offer guidance on how to classify data sensitivity. It does provide a recommendation on how to express access constraints based on a data provider's pre-existing data sensitivity classification. It doesn't explain when, why or how an ethics approval is needed. It does provide a recommendation for the standard machine-readable policy that would tell a data requester that an ethics approval is needed in order to retrieve the data.

In scope for this recommendation are:
- The standard expression of access policies
- The “publishing” of those policies
- The automated execution of machine-readable access policies.

Useful enablers of an access policy but 'out of scope' for this recommendation are:
- How access policies are derived
- How to classify of the sensitive nature of the data
- How to assess the risk of secondary disclosure
- Licences / Legal Agreements /IP / Copyright
- Good practice IT Security/ cybersecurity
- Consent/ Ethics Approval.

## High-Level Recommendation
To promote interoperability and mutual intelligibility around access conditions, CDIF recommends use of the [Open Digital Rights Language (ODRL)](https://www.w3.org/TR/odrl-model/) to describe data asset access policies. ODRL is a RDF-based, 'widely adopted language for expressing permissions, obligations, and conditions related to digital rights' ([Policy Patterns for Usage Control in Data Spaces, 2023](https://arxiv.org/pdf/2309.11289.pdf) ) that can be serialised in JSON and XML. While minimal in terms of classes and relationships, it nonetheless allows sufficient flexibility through the use of constraints and refinements and descriptive logic. ODRL also allows straightforward extensions to the core model and vocabulary with ODRL Profiles.

## Risks and Enablers for CDIF Using ODRL
The existence of ODRL as an existing, well-supported W3C standard is a key 'enabler' for CDIF, based on the the stated [principle](#mainstream) committed to using existing, well-supported standards wherever possible. The first risk with ODRL is that it doesn’t cover all scenarios. The scenario-based discussion in following sections aim to tease out what can be done with ODRL immediately and what scenarios might need further extensions or new approaches. Our conclusion is that  ODRL and its extension/profiling capability is quite useful as is. The second risk is the barrier to adoption of ODRL. There is an urgent need for tooling to simplify how domain scientists and data curators use this mature W3C standard. The information model, ontology, and linked data implementation are beyond the capability of many scientists and infrastructure service providers who can benefit from standardised access policies at scale. This risk is both high and likely and currently has no mitigation.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrlaggregateaccessconditions.md

# Aggregate Access Conditions - Parties and Actions 

A data user wants to query the CESSDA catalogue to find assets useful to address specific data reuse requirements.  The metadata associated with discovered resources should provide a machine-actionable specification of access requirements. 

 The [CESSDA Catalogue](https://datacatalogue.cessda.eu/) is an aggregated social science data catalogue  populated with metadata from 19 European Service Providers (SPs). These SPs provide discovery metadata in either [DDI Codebook](https://ddialliance.org/Specification/DDI-Codebook/2.5/) or [DDI Lifecycle](https://ddialliance.org/Specification/DDI-Lifecycle/3.2/) with consistency assured by the use of [DDI Profiles](https://github.com/cessda/cessda.metadata.profiles). In this catalog metadata relating to access is framed in free text in an XML element, e.g., dcterms:accessRights or ddi:accessRights. This free text does not supply a data consumer with specific, structured information about how they should access data and under what conditions. The practical consequence of this is that a researcher will commonly be directed to another Service Provider's catalogue, and might then find that the dataset of interest requires a formal application process, or might not even be available to them as a citizen of another country.

 There is currently no filter on the CESSDA Catalogue for 'access conditions' because of the heterogeneity of access descriptions that are supplied by multiple SPs. One possible approach is to overlay this heterogeneity with two top-level labels 'Open', and 'Restricted' cf. [CESSDA Data Access Policy](https://zenodo.org/record/6722000) to organise the unstructured prose items into two groups where the border between 'Open' and 'Restricted' is fuzzy.  Another possible access scenario for CESSDA repositories involves making datasets available on the basis of a researcher’s country location before the researcher is permitted to download the data. Again, the CESSDA catalogue metadata schema does not provide a way to specify location-based restrictions on access. The user must drill down into the metadasta and read the licence/rights/access prose for each individual dataset.

Conventions for ODRL policies to express the above access conditions could support more granular groupings of datasets based on their common access features. Re-usable ODRL policies could be deployed across multiple repositories enabling a metadata harvester to aggregate content about access and make access conditions transparent for users searching the catalogue.

At a minimum, this would require referencing a number of standard items such as ODRL ‘Parties’ or ODRL ‘Actions’ by URI.

Formalising access descriptions with a common set of semantics and syntax such as ODRL would enable a discovery metadata aggregator, such as the CESSDA Catalogue, to aggregate content about access, making access conditions more transparent at the point of aggregation.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrlfederatedanalysis.md

# Federated Analytics

Federated analytics is an approach to reuse data without moving the data from the place where it is stored, allowing reuse of sensitive data in its original format. This is a privacy-by-design approach designed to prevent the reverse engineering of individual data centres, sets, and subjects. This is also a useful approach when data are too large to move. 

Federated analytics enables real-time use of a living dataset, in contrast to approaches where a time-fixed version of a dataset is submitted to a repository or trusted research environment and subsequently shared. It is an important tool for analysis of time-varying sensitive data, for example in the health data space. Federated analytics can allow participant-level data to be analyzed across hospitals even though data can not be transferred from one hospital to another because of local data protection legislation. This is predicated on interoperable, high quality data described by interoperable, high quality, rich metadata. 

Federated analytics generally require two levels of permissions. The first is the level of the research question and initiative, i.e., this specific group of data assets can participate in initiatives to answer a given research question. The second level specifies access conditions at the individual asset level. Although humans are engaged in assigning permissions for data assets, federated analytics is dependent on machine-to-machine communication of the types of actions possible for the data assets that are queried in the federated analysis.  The data user is a software agent, and  machine-actionable access policies are required during a machine-to-machine transaction to verify the identity of the agent, allow access to the target data asset(s), and check that the actions performed are those that are allowed.

Federated analysis of sensitive data needs to be accompanied by machine-actionable permissions for common work flows to allow machines to authorize actions on data assets based on rules defined for the specific interactions contributing to the analysis. The current ODRL 2.2 list of Actions for Rules does not include any Actions relevant to analytics. This Scenario highlights the need for extending this vocabulary with actions relevant to federated learning or other analytical processes. ODRL coupled with a structured, machine-readable representation for workflow execution is a necessary part of federated approaches to data reuse. An extended typology of Actions needs to be developed for distributed analytics (as part of a CDIF profile).

Data access policies and rules might constrain software Agents to accessing only parts of a dataset for particular users or analytic workflows. For example to only query a limited set of variables.  ODRL permissions and prohibitions need to consider the processing involved in data analysis and model building, as well as privacy preservation concerns as part of the policy action. This requires Policy makers to specify sub-sets or sub-structures of their data Assets with interoperable, machine-actionable representations. In a federated learning approach to data sharing, refinement of Asset descriptions, e.g. using the DDI-CDI variable model, is necessary to support these more granular access constraints for distributed analytics.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrlincdif.md

# ODRL Implementation

## Policy Example
Ahe data custodians can use ODRL to express a data asset access policy decomposed into specific access conditions, assets, actors, and actions.  This example is based on research environment in Australia.

- **Actor**: Registered academic researchers (ANU_Registered_Users), condition: demonstrate accreditation by ANU (Accredited_Researcher_Property)
- **Action**: analyse dataset in a TRE environment (Analyse_In_TRE)
- **Asset**: dataset 6123 (http://example.com/dataset_6123)
- **Asset**: Pseudonymized data product (http://example.com/dataset_6123; not identified separately)
- **Action**: Secondary use of asset (SecondaryUse)

```
{
"@context": "http://www.w3.org/ns/odrl.jsonld",
"@type": "Set",
"uid": "http://example.com/policy:1",
"permission": [
	{
	"target": "http://example.com/dataset_6123",
	"action": "Analyse_In_TRE",
	"assignee": {
		"@type": "PartyCollection",
		"source": "ANU_Registered_Users",
		"refinement": [
			{
			"leftOperand": "Accredited_Researcher_Property",
			"operator": "eq",
			"rightOperand": "true"
			}
		]
	  }
	},
	{
	"target": "http://example.com/dataset_6123",
	"action": "SecondaryUse",
	"assignee": {
		"@type": "PartyCollection",
		"source": "ANU_Registered_Users",
		"refinement": [
			{
			"leftOperand": "Researcher_Location_Property",
			"operator": "eq",
			"rightOperand": "Australia"
			}
			]
		}
	}
	]
}
```
Example ODRL Policy.
 
Note that in this example Actions, PartyCollections and Refinements only have local meaning and can only be executed locally. 'Analyse_In_TRE' and 'SecondaryUse' are labels that have no potential for machine-actionability beyond the local repository environment.

## Policy Template

Conventions for ODRL policies to express access conditions could support more granular groupings of datasets based on their common access features. Re-usable ODRL policies could be deployed across multiple repositories enabling a metadata harvesters to aggregate content about access and make access conditions transparent for users searching the catalogue.

This approach uses a vocabulary of common, reusable Actions defined in the [ODRL Core Vocabulary](https://www.w3.org/TR/odrl-vocab/#actionsCommon) to populate the 'action' element. Additional terms can be defined in 'ODRL Profiles' (outside of the scope of this document), an extension mechanism for the core model and vocabulary.

The ODRL syntax is used to assert a generic Party in the 'source' element, and then refines it to a particular subset of parties with attributes in the 'refinement' section.  In practice, there is a finite number of 'refinement' permutations that could be pre-defined and assigned a persistent URI to be used as the 'source' key above alongside the dereferenced {leftOperand, operator, rightOperand} array.

Access policies typically define types of users (parties) and what actions they can, cannot or must perform. This depends on referencing a number of standard ODRL 'Parties' or 'Actions' by URI.

```
"permission": [
{
"target": "http://example.com/example_digital_object",
"action": _Actions_,
"assignee": {
	"@type": "PartyCollection",
	"source": _genericParty_,
	"refinement": [
		{
			"leftOperand": _constraintProperty_,
			"operator": _constraintPredicate_,
			"rightOperand": _constraint_value_
		}
	]
	}
}
]
```

Example. ODRL Policy template for re-usable ‘Parties’ and ‘Actions’

```
"permission": [
{
"target": "http://example.com/example_digital_object",
"action": "http://cdif.org/odrl/1/download",
"assignee": {
	"@type": "PartyCollection",
	"source": "https://cessda.eu/partycollection:312",
	"refinement": [
		{
			"leftOperand": "http://www.w3.org/ns/odrl/2/spatial",
			"operator": "http://www.w3.org/ns/odrl/2/eq",
			"rightOperand": "de"
		}
	]
	}
}
]
```

<div id="exampleconcretepolicy">Example ODRL Policy statement<div>. This policy asserts that users located in Germany have the ‘Download’ permission. The reusable 'PartyCollection' item https://cessda.eu/partycollection:312 (signifying users located in Germany) is re-used from an existing vocabulary used by multiple repositories.

The example here disambiguates prose representation of access policies by using URIs as references to (i) pre-defined process actors (ORDL 'Parties') and (ii) pre-defined procedural steps (ODRL 'Actions'), framed in consistent syntactical way. These examples do not in themselves provide sufficient detail or semantics for automated implementation of complex rule-based workflows across multiple parties. To enable repeatable and consistent implementation of request fulfillments framed by ODRL policies, conventions to invoke machine-actionable workflows are needed, for example using [Common Workflow Language (CWL)](https://www.commonwl.org/), including downstream invocations such as creating on-demand secure analytics environments (Infrastructure-as-code or IaaC).  

A common language for expressing data access policies across the cooperative of data providers using the clearing house is a necessary but insufficient first step. A shared understanding of how policies interface with business processes is also required so that both data provider and the clearing house can be satisfied that request fulfilment was efficient, consistent and auditable.

Taking CDIF to the next level of maturity in the access arena will mean committing to the creation of a CDIF ODRL Profile that extends the core ODRL ontology and vocabulary so that a widely applicable set of cross-domain Actions are available for re-use as well as being associated with unambiguous workflow implementations, expressed with additional classes and attributes in the CDIF ODRL Profile.

##  Connecting CDIF and ODRL

(under construction)
CDIF recommends that a DCAT record be created, describing a dcat:distribution or, in lay parlance, a digital object, corresponding to the data set or resources to be used. For queryable data sources, this would instead be a dcat:service. (The dcat:dataset class is not used, because different distributions of it may have different access conditions.) An ODRL Rule has a mandatory ‘target’ attribute which specifies the ODRL Asset to which the Rule applies. For example:

```
"permission": [
	{
		"target": "http://repository7987.org/dataset_6123",
		"action": "http://cdif.org/odrl/1/download",
		"assignee": "http://orciduser675765",
	}
```

Conversely, a DCAT record could express a predicate http://www.w3.org/ns/odrl/2/hasPolicy with the URI of the ODRL Policy as a target.

An ODRL policy might apply to multiple ODRL Assets. One possible solution is to leverage the ODRL AssetCollection class, which can group multiple Assets under one URI as the target of an ODRL rule. This requires policies defining persistent grouping rules that define an AssetCollection, determining if and how the membership of the AssetCollection can change.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrlinternalpolicies.md

#  Representing Internal Access Policies with ODRL

A standalone repository can hold sensitive personal data requiring mediated access. The target persona might be a data manager in a high profile research group that conducts health studies. The group is committed to providing 'secondary access' to other research groups to build collaborative networks and optimise reuse and impact of data they have collected. The data manager wants make the access processes visible with policies that ensure consistent, efficient processing of access requests, and provide standardised policy types that support automation of access workflows. The research group wants to start with a single policy for its clinical trial datasets (assets) that makes it clear that these datasets are available for secondary use by other academic users. The research group also wishes to specify actions that can be performed on those assets by end users (e.g. access for academic researchers for a specific research question to the full dataset in a trusted research environment (TRE) ).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrloverview.md

# Overview of ODRL

The core classes are:
- **Parties** - actors or agents who exercise:
- **Rules** - ODRL Permissions (can do), ODRL Duties (must do), ODRL Prohibitions (must not do)
encompassing:
- **Actions** - operations performed on:
- **Assets** - digital objects in a CDIF context.
- **Policies** - are structured artefacts that document the above information.

![ODRL class overview](./figures/odrlclasses.jpg)

Figure. Simplified schematic of main ODRL Classes.

## ODRL Resources

ODRL Information Model: https://www.w3.org/TR/odrl-model/

ODRL Core Vocabulary: https://www.w3.org/TR/odrl-vocab/

Example ODRL access policies:
https://fiware-true-connector.readthedocs.io/en/latest/usage_control_rules.html

Arxiv preprint on applying ODRL in Transport Mobility Data Space: https://arxiv.org/pdf/2309.11289.pdf

ODRL Policy validator: https://odrlapi.appspot.com/

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/odrlsharedservices.md

# Conventions for ODRL Parties and Actions

A data clearing house can aggregate metadata from many repositories and broker access to resources in those repositores. Conventions for representing data access policies are necessary to support groupings of datasets based on their common access policies. Re-usable ODRL policies could be deployed across multiple repositories enabling a metadata harvester to aggregate content about access and make access conditions transparent for users searching the catalogue. The benefits of such a clearing house approach could include:
- Streamlining processes for data users
- Support for combined interdependent requests across multiple data providers for complex studies
- Efficiencies of resourcing and specialisation
- Natural combined reporting and tracking of usage and impact

Standardised, machine-actionable data access policies necessary to deliver on two assumptions of a shared clearing house:
- that the cost of sharing the information about requests does not overwhelm the savings in staff and systems.
- That a central capability can action things and lighten the load of the network rather than just re-routing jobs for fulfilment back to the participating node for 'local implementation'.

The basic approach to representing policies that can be implemented with existing ODRL technology is described in [ODRL implementation](./odrlincdif.md).


# Workflow Scenario:
The workflow outlined in the table below illustrates a message exchange initiated by a researcher requesting a dataset stored in a specific repository with a central clearing house mediating access on behalf of this and many other repositories. Note that here, the Broker (clearing house) is not acting as a portal for finding the data, but as a mediator of access to a resource known to be at an identified repository.

| **step** | **Message** | **Message pseudo-description** |
| --- | --- | --- |
1 |Request CDIF Resource|User locates dataset resource on repository catalogue with DOI https://dx.doi.org:12345 and clicks on ‘Access Data’ button
2 |CDIF ODRL Policy|Repository posts new RequestFulfilment object to Brokerage API including location of CDIF record for https://dx.doi.org:12345, a JSON-LD artefact which encapsulates ODRL Policy #2b
3 |Request AgentProperties|Brokerage parses the ODRL Policy statement and determines that the user must be located in Germany. More complex real-world examples might be the collection of additional information through an online form managed by the broker.
4 |Supply AgentProperties|The user will supply any information requested by the broker.
5 |Verify AgentProperties|The brokerage will perform the necessary validation and verification of any information supplied by the user. This might involve auxiliary processes, such as seeking third party approval.
6 |ODRL Request|Once all conditions outlined by the ODRL Policy have been met and satisfied by the broker, an ODRL Request will be sent to the repository on behalf of the user.<br>{ "@context": "http://www.w3.org/ns/odrl.jsonld",<br>"@type":"Request",<br>"uid":"http://brokerage.com/odrlrequest/9a112bc6-d93d-4a59-8384-0ac65399ef94", <br>"permission": [<br>&emsp;{"target": "http://repository7987.org/dataset_6123",<br>&emsp;"action": "http://cdif.org/odrl/1/download", <br>&emsp;"assignee": "http://orciduser675765"}<br>&emsp;]}
7 |ODRL Offer|The repository will respond with an ODRL Offer to the broker.<br>{"@context": "http://www.w3.org/ns/odrl.jsonld", <br>"@type": "Offer",<br>"uid":"http://brokerage.com/odrloffer/2f93930b-93f7-418f-a045-aa49d09faf2b", <br>"permission": [<br>&emsp;{"target": "http://repository7987.org/dataset_6123", <br>&emsp;"action": "http://cdif.org/odrl/1/download", <br>&emsp;"assigner": "http://repository7987.org"}<br>&emsp;]}
8 	|AccessToken and ODRL Agreement |	Assuming the broker accepts the offer on behalf of the user, an encrypted Access token is sent to the user and an ODRL Agreement is filed for audit purposes.<br>{<br>"@context": "http://www.w3.org/ns/odrl.jsonld",<br>"@type": "Agreement",<br>"uid":"		http://example.com/odrlagreement/d91d4663-f9bd-4bd5-8a81-c331e19bf987",<br>	"dcterms:references":[<br>&emsp;"http://brokerage.com/odrlrequest/9a112bc6-d93d-4a59-8384-0ac65399ef94",<br>		&emsp;"http://brokerage.com/odrloffer/2f93930b-93f7-418f-a045-aa49d09faf2b"<br>&emsp;],<br>	"permission": [<br>	&emsp;{"target":"http://repository7987.org/dataset_6123",<br>&emsp;"action": "http://cdif.org/odrl/1/download",<br>&emsp;"assigner": "http://repository7987.org",<br>&emsp;"assignee": "http://orciduser675765"}<br>&emsp;]}
9 |Present Access Token|The user presents the token to the Repository
10|Retrieve Resource|The repository makes the file available for immediate download to the user.


This is over-engineered for a simple download where the only condition is that the researcher be based in Germany. Practical access policies are likely to require multi-step processes with complex criteria, often with asynchronous handoffs to third parties for approval. The framework above, while necessarily brief for the purposes of this document, illustrates how a more complex stateful negotiation process could be performed using ODRL as the basis for defining conditions,  executing those conditions through a centralised brokerage, and generating a rich set of accounting information for access requests and fulfilment across the supported repositories.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_access/policies.md

# Data Access Policies

## Data Provider vs. Data User Access Policies
ODRL data access policies can be formulated or executed by either the data provider or the data user. For example, a data user may establish an ODRL policy that requires the data to conform to a certain standard as part of a machine readable request. Because of the audience and context of CDIF, this document starts from the perspective of the data policies of the data provider, since they fit in with the perspective of a metadata standard for interoperability being established for/by data providers.

## Access Classifications
It is not uncommon for data providers (or communities thereof) to apply broad 'access classifications' to data, for example:
● openAccess / restrictedAccess [CESSDA](https://www.cessda.eu/)
● Open / Safeguarded / Controlled [UKDS](https://ukdataservice.ac.uk/)
● ClosedAccess / EmbargoedAccess / RestrictedAccess / OpenAccess [OpenAIRE](https://www.openaire.eu/)

When included in discovery metadata, such classifications drive useful functionality in portals or catalogues for filtering or faceting search results. They are not sufficient however to drive automatable access processes. Machine-actionable access policies are inherently more fine grained than such high level classifications and involve a number of top level entities (parties/actions/rules) over sequenced workflows (request/access/usage). It would not be practical to create a top-down classification system granular enough and with broad enough consensus to drive machine actionable access policies. Rather the recommendation here is to use a standardised and structured language for access policies so that these can be generated bottom-up and yet retain the appropriate level of interoperability.

## Access Policy Scenarios and Recommendations
This section discusses several situations dealing with sensitive data for with access policies are necessary.
1. A standalone repository holding sensitive personal data wishes to provide 'secondary access' to other research groups. [Standalone repository](./odrlinternalpolicies.md)
2. A metadata aggregator wants to provide search clients with filters based on access policies [Metadata aggregator](./odrlaggregateaccessconditions.md)
3. A central clearing house mediating access to data in federated repositories [Mediated access](./odrlsharedservices.md)
4. Federated analysis over multiple sensitive data providers [Federated analytics](odrlfederatedanalysis.md)

These scenarios build a set of typical requirements for the interoperability of access policy summarised in the figure below.

![Data access scenarios](./figures/dataaccessscenarios.jpg)

Figure. Data access scenarios

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_description/archive/ddiclassesandproperties.md




---
### Source Document: data_description/dataStructureSchemaImplementationNew.md

# CDIF Data Structure Profile — Schema.org Implementation

This page documents the content items in the CDIF Data Structure profile and how each is encoded in JSON-LD. Some example metadata documents are accessible in the [Data Structure GitHub repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/tree/reviewRevision202606/examples). The 'Cardinality' value specifies how many values a property may carry: `1` means one value required; `1..*` means at least one required, repeatable; `0..*` means optional and repeatable; `0..1` means optional, single-valued.

All property names use namespace prefixes as declared in the `@context` (e.g. `schema:`, `dcterms:`, `cdi:`, `cdif:`). The CDIF JSON-LD implementation uses a hierarchical JSON structure, and CURIE syntax to abbreviate URIs using prefixes defined in the JSON-LD context. The implementation does not map un-prefixed JSON keys to URIs; rather, it prefixes a namespace abbreviation on the key label to represent the URI. This enables using standard JSON Schema to validate documents and avoids confusion about the vocabulary origin of keys used in the JSON.

The Data Structure profile builds on the CDIF Data Description profile (which describes what a dataset's variables *are*) and adds *what roles those variables play in the dataset's structure and how records are keyed*. A `schema:DataDownload` distribution gains a `cdi:isStructuredBy` link pointing to one of three concrete structures — `cdi:WideDataStructure`, `cdi:LongDataStructure`, or `cdi:DimensionalDataStructure` — each of which lists the role-typed components that make up the structure.

Each item lists its Cardinality, JSON encoding, and a Description explaining usage.

See also [graphical presentation of the Data Structure profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataStructure/index.html)

Artefacts for the Data Structure profile are in this [GitHub repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/tree/reviewRevision202606) (TBD — update link to release tag).

The profile's authoritative implementation guide is [CDIFDataStructureImplementationGuide.md](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructureImplementationGuide.md); this page is a content-item-focused summary derived from it.


## Profile conformance declaration
- **Cardinality:** 1..*
- **JSON:**
  ```json
  "schema:subjectOf" / "dcterms:conformsTo": [
    {"@id": "https://w3id.org/cdif/data_structure/1.1"}
  ]
  ```
- **Description:** Required URI declaring that the metadata record conforms to the Data Structure profile. Add to the `dcterms:conformsTo` array on the catalog record alongside conformsTo identifiers for any other profiles that are also being asserted (Core, Discovery, Data Description, etc.). Note that the CDIF conformance class URIs are registered such that the base URI (e.g. https://w3id.org/cdif/data_structure/1.1/) resolves to this implementation guidance page; add /schema and the uri will resolve to the JSON schema for validating instance documents using that profile; add /shacl and the shacl rules, encoded in turtle format, will be returned.

## Distribution data structure link
- **Cardinality:** 1 per conforming DataDownload
- **JSON:**
  ```json
  "schema:distribution": [{
    "@type": ["schema:DataDownload"],
    "schema:contentUrl": "...",
    "cdi:isStructuredBy": { /* inline DataStructure */ }
  }]
  ```
- **Description:** Each `schema:DataDownload` distribution that conforms to this profile must carry a `cdi:isStructuredBy` value that is either an inline `cdi:WideDataStructure`, `cdi:LongDataStructure`, or `cdi:DimensionalDataStructure`, **or** an `@id` reference to a DataStructure defined elsewhere (in the same document, or accessible on the web). Using an `@id` reference is the way the same reusable structure is shared across multiple distributions or datasets.

## Wide data structure
- **Cardinality:** referenced
- **JSON:**
  ```json
  {
    "@type": ["cdi:WideDataStructure"],
    "@id": "#wide-structure-1",
    "cdi:has_DataStructureComponent": [ /* IdentifierComponent, MeasureComponent, AttributeComponent */ ],
    "cdi:has_PrimaryKey": { /* PrimaryKey */ }
  }
  ```
- **Description:** Structure of a one-row-per-unit dataset. Each record represents properties of one unit in the population. Components must each be one of `cdif:IdentifierComponent`, `cdif:MeasureComponent`, or `cdif:AttributeComponent`. `cdi:has_PrimaryKey` and `cdi:has_ForeignKey` are optional.

## Long data structure
- **Cardinality:** referenced
- **JSON:**
  ```json
  {
    "@type": ["cdi:LongDataStructure"],
    "@id": "#long-structure-1",
    "cdi:has_DataStructureComponent": [ /* IdentifierComponent, VariableDescriptorComponent, VariableValueComponent, AttributeComponent */ ]
  }
  ```
- **Description:** Structure of an entity-attribute-value ("long") dataset. Each row contains an identifier, a code naming a variable, and the value of that variable for the identified unit. Components must each be one of `cdif:IdentifierComponent`, `cdif:VariableDescriptorComponent`, `cdif:VariableValueComponent`, or `cdif:AttributeComponent`. Primary/foreign keys are optional.

## Dimensional data structure
- **Cardinality:** referenced
- **JSON:**
  ```json
  {
    "@type": ["cdi:DimensionalDataStructure"],
    "@id": "#cube-structure-1",
    "cdi:has_DataStructureComponent": [ /* DimensionComponent, MeasureComponent, AttributeComponent */ ],
    "cdi:has_DimensionGroup": [ /* DimensionGroup */ ]
  }
  ```
- **Description:** Structure of a multidimensional ("cube") dataset. Each record is addressed by a set of dimension values. Components must each be one of `cdif:DimensionComponent`, `cdif:MeasureComponent`, or `cdif:AttributeComponent`. `cdi:has_DimensionGroup` groups dimensions that together address a coordinate position.

## Identifier component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 1..*
- **JSON:**
  ```json
  {
    "@type": ["cdif:IdentifierComponent"],
    "cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-unit-id"}
  }
  ```
- **Description:** Role given to a represented variable that provides identifying values for records. Used in `cdi:WideDataStructure` and `cdi:LongDataStructure`. `cdif:isDefinedBy_RepresentedVariable` is required.

## Measure component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 0..*
- **JSON:**
  ```json
  {
    "@type": ["cdif:MeasureComponent"],
    "cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-temperature"},
    "cdi:semantic": ["http://qudt.org/vocab/quantitykind/Temperature"]
  }
  ```
- **Description:** Role given to a represented variable that holds the observed or derived values of the dataset. Permitted in `cdi:WideDataStructure` and `cdi:DimensionalDataStructure`. (In `cdi:LongDataStructure` the measured value is carried by `cdif:VariableValueComponent` instead.) The optional `cdi:semantic` carries one or more IRIs or `cdifConceptOrTerm` references that qualify the purpose of the measure against an external controlled vocabulary.

## Attribute component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 0..*
- **JSON:**
  ```json
  {
    "@type": ["cdif:AttributeComponent"],
    "cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-uncertainty"},
    "cdi:qualifies": [{"@id": "#component-temperature"}]
  }
  ```
- **Description:** Role given to a represented variable that qualifies observations or provides supplementary information (e.g. uncertainty, quality flag, observation method). Permitted in all three concrete DataStructure subtypes. `cdi:qualifies` optionally points to the component(s) being qualified.

## Dimension component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 1..* (in DimensionalDataStructure)
- **JSON:**
  ```json
  {
    "@type": ["cdif:DimensionComponent"],
    "cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-time-bin"}
  }
  ```
- **Description:** Role given to a represented variable that acts as a coordinate axis in a multidimensional structure. Used only in `cdi:DimensionalDataStructure`. Dimensions are typically categorical (codelist-valued) or quantized continuous variables (e.g. time bins). `cdif:isDefinedBy_RepresentedVariable` is required.

## Variable descriptor component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 1 (in LongDataStructure)
- **JSON:**
  ```json
  {
    "@type": ["cdif:VariableDescriptorComponent"],
    "cdif:isDefinedBy_DescriptorVariable": {
      "@type": ["cdi:DescriptorVariable"],
      "cdif:name": ["variable_name"],
      "cdif:hasValuesFrom": { /* DescriptorValueDomain mapping codes to RepresentedVariables */ }
    }
  }
  ```
- **Description:** Role given to a represented variable that holds codes identifying *which* logical variable a given long-format row records. Used only in `cdi:LongDataStructure`. `cdif:isDefinedBy_DescriptorVariable` is required and carries an inline `cdi:DescriptorVariable` whose `cdif:hasValuesFrom` is a `cdi:DescriptorValueDomain` enumerating the codes that can appear in the descriptor column, each paired (via `cdif:isDefinedBy`) with the represented variable the code names.

## Variable value component
- **Cardinality:** within `cdi:has_DataStructureComponent`, 1 (in LongDataStructure)
- **JSON:**
  ```json
  {
    "@type": ["cdif:VariableValueComponent"],
    "cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-value"}
  }
  ```
- **Description:** Role given to a represented variable that carries the value of whichever logical variable the row's descriptor identifies. Used only in `cdi:LongDataStructure`. Paired with a sibling `cdif:VariableDescriptorComponent` in the same row.

## Dimension group
- **Cardinality:** in DimensionalDataStructure, 0..*
- **JSON:**
  ```json
  "cdi:has_DimensionGroup": [{
    "@type": ["cdi:DimensionGroup"],
    "@id": "#time-group",
    "cdi:has_DimensionComponent": [{"@id": "#year"}, {"@id": "#month"}, {"@id": "#day"}]
  }]
  ```
- **Description:** Groups dimension components that together address a coordinate position (e.g., a `time` group of year/month/day, a `geography` group of country/state/county). `cdi:has_DimensionComponent` references the grouped dimensions.

## Primary key
- **Cardinality:** 0..1 per DataStructure
- **JSON:**
  ```json
  "cdi:has_PrimaryKey": {
    "@type": ["cdif:PrimaryKey"],
    "cdif:isComposedOf": [
      {"cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-county-fips"}},
      {"cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-year"}}
    ]
  }
  ```
- **Description:** Ordered set of represented variables whose values uniquely identify a record. Array order in `cdif:isComposedOf` is the key position (no intermediate ComponentPosition wrapper). Each item references the represented variable that plays that key position.

## Foreign key
- **Cardinality:** 0..*  per DataStructure
- **JSON:**
  ```json
  "cdi:has_ForeignKey": [{
    "@type": ["cdif:ForeignKey"],
    "cdif:isComposedOf": [
      {"cdif:isDefinedBy_RepresentedVariable": {"@id": "#var-county-fips"}}
    ],
    "cdi:references": {"@id": "https://example.org/datasets/census2020#primary-key"}
  }]
  ```
- **Description:** Set of represented variables in this dataset whose values match a primary key in another dataset. `cdi:references` is an `@id` reference to the primary key of the referenced dataset.

## Represented variable
- **Cardinality:** referenced from each component via `cdif:isDefinedBy_RepresentedVariable`
- **JSON:**
  ```json
  {
    "@type": ["cdif:RepresentedVariable"],
    "@id": "#var-temperature",
    "cdif:name": ["air_temperature"],
    "cdif:displayLabel": ["Air temperature"],
    "cdif:definition": "Dry-bulb air temperature measured 2 m above ground.",
    "cdi:hasIntendedDataType": "xsd:double",
    "cdi:simpleUnitOfMeasure": "K",
    "cdi:unitOfMeasureKind": "temperature",
    "cdi:takesSubstantiveValuesFrom": {"@id": "#valuedomain-temperature"}
  }
  ```
- **Description:** A conceptual variable bound to a substantive value domain — *logical* in the sense that it is not tied to a particular physical data type or column position. The same RepresentedVariable can be referenced from components in wide / long / dimensional structures; that's what lets the same dataset be presented in more than one layout. Cardinality of inner properties is mostly `0..1`; see the [Implementation Guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructureImplementationGuide.md#cdifrepresentedvariable) for the full set.

## Variable substantive value domain
- **Cardinality:** 0..1 per RepresentedVariable
- **JSON:**
  ```json
  "cdi:takesSubstantiveValuesFrom": {
    "@type": ["cdi:SubstantiveValueDomain"],
    "@id": "#valuedomain-temperature",
    "cdif:recommendedDataType": ["xsd:double"],
    "cdi:isDescribedBy": {
      "@type": ["cdif:ValueAndConceptDescription"],
      "cdi:classificationLevel": "Ratio",
      "cdi:minimumValueInclusive": "0"
    }
  }
  ```
- **Description:** The set of valid, meaningful values for this variable. Either references a `cdif:EnumerationDomain` (for codelist-valued variables) via `cdif:takesValuesFrom`, or is described by a `cdif:ValueAndConceptDescription` (for continuous, ordinal, or pattern-constrained variables) via `cdi:isDescribedBy`.

## Variable sentinel value domain
- **Cardinality:** 0..* per RepresentedVariable
- **JSON:**
  ```json
  "cdi:takesSentinelValuesFrom": [{
    "@type": ["cdi:SentinelValueDomain"],
    "cdif:takesValuesFrom": {"@id": "#missing-codes-codelist"}
  }]
  ```
- **Description:** The sentinel (missing / not-applicable / N/A code) value domain of a RepresentedVariable. May reference one or more distinct sentinel domains (e.g., one codelist for "missing", another for "not applicable").

## Enumeration value domain
- **Cardinality:** referenced
- **JSON:**
  ```json
  {
    "@type": ["cdif:EnumerationDomain"],
    "schema:name": "Census 2020 county codes",
    "cdif:references": {"@id": "https://example.org/codelists/county-fips"},
    "cdif:purpose": "Allowed county identifiers for U.S. data"
  }
  ```
- **Description:** A wrapper allowing a CDIF Codelist (a `skos:ConceptScheme` per the Codelist profile) to be documented as an enumerated value domain. `cdif:references` is required and points to the codelist whose `skos:notation` values are the allowed values of this enumeration.

## Value description (non-enumerated)
- **Cardinality:** 0..1 per SubstantiveValueDomain
- **JSON:**
  ```json
  "cdi:isDescribedBy": {
    "@type": ["cdif:ValueAndConceptDescription"],
    "cdi:classificationLevel": "Continuous",
    "cdi:formatPattern": "#,##0.###",
    "cdi:minimumValueInclusive": "0",
    "cdi:maximumValueExclusive": "100",
    "cdi:regularExpression": "^[0-9]+(\\.[0-9]+)?$"
  }
  ```
- **Description:** Formal description of a non-enumerated value space, used when the substantive value domain is characterized by ranges, patterns, expressions, or classification level rather than a discrete list. `cdi:classificationLevel` is one of `Continuous`, `Interval`, `Nominal`, `Ordinal`, `Ratio`.

## Variable unit of measure
- **Cardinality:** 0..1 per RepresentedVariable
- **JSON:**
  ```json
  "cdi:simpleUnitOfMeasure": "K"
  ```
  or
  ```json
  "cdi:describedUnitOfMeasure": {"@id": "http://qudt.org/vocab/unit/K"}
  ```
- **Description:** Unit of measure for the variable's values. Use `cdi:simpleUnitOfMeasure` (string) for a simple label or symbol; use `cdi:describedUnitOfMeasure` (string IRI or `cdifConceptOrTerm` reference) for a structured unit drawn from a controlled vocabulary (e.g. QUDT). `cdi:unitOfMeasureKind` (e.g., "temperature", "salinity") can be added to allow translation between equivalent units.

## Variable intended datatype
- **Cardinality:** 0..1 per RepresentedVariable
- **JSON:** `"cdi:hasIntendedDataType": "xsd:double"`
- **Description:** Intended physical datatype for variable values. Use an `xsd:` datatype IRI, or a `cdifConceptOrTerm` reference for richer typing.

## Component semantic tag
- **Cardinality:** 0..* per component
- **JSON:** `"cdi:semantic": ["http://qudt.org/vocab/quantitykind/Temperature"]`
- **Description:** Qualifies the role-typed purpose of a component using one or more external controlled-vocabulary IRIs or `cdifConceptOrTerm` references. Allowed on `cdif:MeasureComponent`, `cdif:AttributeComponent`, `cdif:VariableDescriptorComponent`, `cdif:VariableValueComponent` (and on `cdif:DimensionComponent` indirectly via its represented variable).

## Component identifier
- **Cardinality:** 0..1 per component
- **JSON:** `"cdi:identifier": {"@id": "https://example.org/idmint/component-12345"}`
- **Description:** Optional reusable identifier for a component, allowing the same component definition to be referenced from multiple data structures. Value is an `@id` reference to a `schema:Identifier` (PropertyValue pattern).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_description/datadescriptionforintegration.md

# Describing Data: Data Sets and Data Structures

This version of the CDIF recommendations does not contain a full profile for the description of data integration, but this topic has received a lot of attention from the working group. An exploration into different data integration scenarios has been conducted, notably an effort to integrate data from ILO, the World Health Organization (WHO), and the SDG Indicators, with a goal of publishing this data into Google Data Commons and the knowledge graph model used there. This work is on-going, but it has demonstrated the set of metadata needed to fully describe a data integration.

This set of metadata requirements can be summarised as follows, based on the assumption that there is access to the data being integrated:
1. Detailed data description (variable-level)
2. Structural metadata of the data sets
3. Enumerated values (codelists and classifications)
4. Mappings between sets of enumerated values
5. Processing description, indicating how mappings were implemented in transformations, and what other operations were performed for data integration

While this seems like a daunting set of information, the exploratory work has shown that if the metadata are available in a sufficiently detailed form, then the actual integration itself is straightforward.

A data provider is expected to describe the data as they manage and present it, along with information about its logical contents. The user can then re-structure the data as needed for their own use, and do so programmatically. Sufficient metadata must be available to support this programmatic restructuring, without losing any of the information about the data - especially its links to semantic definitions.

The concept definitions that specify semantics must be separated from the structural description of data for a useful cross-domain data description scheme, along with an indication of where the semantics for both the field and the values come from. 

In the current release, we provide profiles for describing data sets - including a minimal structural description - in the Data Description profile, and a means of describing reusable (or more complex) data structures and harmonized, reusable variables in the Data Structures profile.

# Data Structure Basics

A dataset provides values for a set of variables that characterize some unit of interest. Each record in the dataset is about a particular unit or individual in the world. In the CDIF framework, a data descovery description provides basic information about the units that are the subject of a dataset, and can provide a list of variables associated with those units. The data description profile provides information about the physical representation of the values for variables, and how they are arranged to serialize in a file that can be shared between computer systems.  

The DDI-CDI model provides a framework for describing data structures. A foundation concept is the variable cascade.  A variable can be defined at the conceptual level-- independent of any particular approach to representing values the variable might have. Temperature could be considered a conceptual variable.  Conceptual variables can be represented in inforamtion systems in various ways.  Temperature can be represented with categories like 'really hot', 'hot', 'cold', or numerically with one of several quantitative scales like kelvin or farenheit. A represented variable specifies how a conceptual variable's values are quantified in an implementation independent way. A set of temperature categories can be represented using a different vocabularies; quantitative temperatures might be represented as integers or decimal numbers. An instance variable specifies a the implementation of a represented variable in a particular data set-- the exact set of strings used to represent categories, data types that are defined in programming languages, constraints on string lengths, constraints on string syntax using regular expressions, etc. 

Another foundation concept useful for describing data structures is the data structure component.  Variables in a data structure have different roles in their relationship to description of the unit that is the subject of a record. Key roles include:
- identifier: variables that serve to uniquely identify the individual that is the subject of a record
- measure: variables that quantify properties of the subject of the record
- attribute: variables that qualify the values of other variables in the dataset. 
- reference: variables the provide identifiers for linking between datasets. 
- Other more complex roles will be described later.

The data description profile is focused on describing the physical implementation of variables in a particular dataset, based on a set of instance variable descriptions and a physical mapping that documents how the values of variables and their binding to individual records are located in a file containing the dataset. The data structure profile provides a way to describe a dataset that can be applied to more than one dataset instance, using represented variables and data structure components. We will refer to this 'portable' data structure description as a logical data structure.  

# Data Description Workflow

CDIF recommends a subset of the classes in the DDI-CDI specification for data description.  For a static set of data there are four steps. For a service, where the structure and physical format of the data will depend on the service, the last two steps are not required.

The process for providing such detailed descriptions of data can be broken down into a series of steps:
1. **Describe the Data Set or Service**: Identify the logical variables in the data, where each 'variable' measures a single characteristic of a single unit type, using a consistent set of values. The possible values must be enumerated or otherwise described in a detailed fashion. Representations must be able to identify domain-agnostic semantic descriptions for each possible value, and the variable definitions themselves must similarly be independent of any domain specificity.
2. **Describe the Variables**: Indicate how the logical variables fit into the structure of the file, by specifying also any 'presentational' variables used for structuring the data serialization in a file. Relationship between presentation and logical variables must be specified. The complete set of variables can then be described as a 'logical record'.
3. **Describe the Data Structure**: Including the fields used to identify a record (the 'primary key').
4. **Describe the Physical Format of the Data**: Describe the encoding of all variables physically present in the file, and how they are sequenced and stored for programmatic retrieval.

# Mappings

It is recognized that transformations to both data and metadata at several levels are a critical part of data integration. The mappings used to inform transformations are a critical aspect of this, being both needed provenance information and also potentially providing a reusable FAIR resource in their own right. There is an RDA group working on [FAIR Mappings](https://mapping-commons.github.io/rda-fair-mappings/use-cases/), and the CDIF WG follows this work and attempts to align with it. Currently, the use of A Simple Standard for Sharing Ontology mappings ([SSSOM](https://mapping-commons.github.io/sssom/dev/)) is seen as a useful standard for the expression of mappings, with the RDF Mapping Language [RML](https://rml.io/specs/rml/) also proving to be of interest, This is an area where motre work remains to be done, but will be the subject of a CDIF profile in the not-too-distant future.

# Processing Description
In CDIF, the description of processing is understood to be a primary aspect of data provenance. As such, it will be addressed by its own profile in future. There is some provision for provenance information in CDIF now, but this aspect of data integartion will be more completely addressed by the firthcoming profile.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_description/datadescriptionprofile.md

# Data Description Profile

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/cdifDataDescriptionStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/CDIFDataDescriptionImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/dataDescriptionRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/cdifDataDescription-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataDescription/index.html)

This profile specifies metadata for describing quantitative data sets at a detailed level, sufficient to support the machine-to-machine exchange of data for processing, including links to all needed semantic artefacts (i.e., codelists, controlled vocabularies) for scientists to understand the data. The emphasis is on structural metadata describing a physical dataset instance,  to enable parsing and re-organizing data for use. The profile covers the description of wide ("unit record") data sets, long (event stream) data sets, and multi-dimensional data sets ("data cubes"). The profile uses [Schema.org](https://schema.org/) and [DDI-CDI](https://ddialliance.org/ddi-cdi), with a reliance on the Codelist profile for describing enumerated value domains. Documentation of physical dataset structure that is reusable for description of many dataset instance is specified in the Data Structure profile.

Conformance to this profile entails populating all mandatory content from cdifCore, using recommended discovery properties, and providing the additional data description constraints. The implementation target is an rdf serialization, which is an open world logical model; users are thus free to add additional properties that they find useful for dataset documentation in their community, but these can be ignored by other users without penalty.

see also [graphical presentation of Data Description Profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataDescription/index.html)

Artefacts for the Data Description profile are in this [Github repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/tree/reviewRevision202606) (TBD--update link to release tag)

## Requirements

This profile imports all requirements from CDIF Core and CDIF Data Discovery profile. This profile adds additional requirements:

- Define the structure of the serialization used to deliver a specific dataset representation. Focus is on columnar data represented in tables (e.g. csv—any delimited text format.) and multidimensional data represented in structured binary formats (e.g. HDF5, NetCDF). 
- Required properties
- Vocabularies used for enumerated domains
- Locators for variable values within the physical data structure (column number, hdf path…). 
- Datatypes used to represent values
- Domain for values, including substantive and sentinel values, or other restrictions on values (string length, regular expressions)
- Roles of instance variable in the data structure, e.g. measure, unit identifer, attribute, dimension. 
- Primary key-- the variable(s) that uniquely identify each data instance
- Linkage of attribute variable to variable(s) it qualifies. 
- Statistics on InstanceVariables

## Implementation

## class--Dataset properties added in Data Description Profile

(cdifhasprimarykey)=
### cdif:hasPrimaryKey
- **Cardinality:** Optional, Repeatable
- **JSON:** [cdif:Key](#sec-cdifkey)
- **Description:** Primary key of the dataset: a `cdif:Key` whose `cdif:isComposedOf` is an ordered list of `cdi:ComponentPosition` wrappers. Each wrapper carries `cdi:indexes` (the `cdi:InstanceVariable` at that position, drawn from `schema:variableMeasured`, inline or `@id`-reference) and `cdi:value` (the integer position in the key, 0- or 1-based). Together the wrappers identify each data instance. Matches the canonical DDI-CDI PrimaryKey structure defined in `ddi-cdif-data-structure`.


### cdif:statistics
- **Cardinality:** Optional, Repeatable
- **JSON:** [cdi:Statistics](#sec-cdistatistics), [cdi:CategoryStatistics](#sec-cdicategorystatistics), or [cdif:StatisticsCollection](#sec-cdifstatisticscollection); inline or `@id`-reference
- **Description:** Summary statistics describing the dataset's values. Each entry is a `cdi:Statistics` bundle (one or more Statistic value objects, optionally weighted by an InstanceVariable, optionally broken down by Category), a `cdi:CategoryStatistics` (per-category statistics), or a `cdif:StatisticsCollection` (groups multiple Statistics nodes and records which InstanceVariables they index). Either inline a node here, or use an `@id`-reference to one declared elsewhere in the document.


(sec-cdifinstancevariable)=
## class--InstanceVariable
A `schema:variableMeasured` item at the Data Description level is a CDIF profile of the DDI-CDI InstanceVariable. It composes the basic Discovery `variableMeasured` shape ([PropertyValue-(variableMeasured)](#sec-propertyvalue-vm)) and extends it with properties describing the variable's data type, role, source, value domain, weighting, and summary statistics. The schema.org base properties on PropertyValue (`@id`, `schema:name`, `schema:description`, `schema:alternateName`, `schema:propertyID`, `schema:measurementTechnique`, `schema:unitText`, `schema:unitCode`, `schema:minValue`, `schema:maxValue`, `schema:url`) remain available unchanged; the additions below are CDIF-specific.

### \@type
- **Cardinality:** Required, Repeatable
- **JSON:** string.uri
- **Description:** MUST include both `schema:PropertyValue` and `cdi:InstanceVariable`. Additional types may be included.

### cdif:physicalDataType
- **Cardinality:** Optional, Repeatable
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** Identifier or name for the data type concept describing the physical representation of values for this variable.


### cdif:role
- **Cardinality:** Optional
- **JSON:** string (controlled-vocabulary entry)
- **Description:** Specifies the role this variable plays in a data structure. Common values: `UnitIdentifier` (names the unit a row describes), `Measure` (holds observed/derived values), `Attribute` (qualifies an observation), `Dimension` (addresses a position in a multi-dimensional value space).


### cdif:simpleUnitOfMeasure
- **Cardinality:** Optional
- **JSON:** string, [DefinedTerm](#sec-definedterm), or [skos:Concept](#sec-skosconcept)
- **Description:** Simple text-based unit of measure for the values of this variable. For a controlled-vocabulary unit entry, use `cdi:describedUnitOfMeasure` instead.


### cdif:uses
- **Cardinality:** Optional, Repeatable
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** Essentially the same as `schema:propertyID`. References to concepts that this variable measures or represents. When the dataset's distribution carries `cdi:isStructuredBy` (CDIF Data Structure profile), `cdif:uses` connects the InstanceVariable to a reusable RepresentedVariable concept.


### cdif:isDescribedBy_StatisticsCollection
- **Cardinality:** Optional
- **JSON:** [cdif:StatisticsCollection](#sec-cdifstatisticscollection) or [object reference](#object-reference)
- **Description:** The StatisticsCollection holding summary / category statistics for this InstanceVariable (InstanceVariable.isDescribedBy). `cdif:` namespaced and target-suffixed because the DDI-CDI `isDescribedBy` association is polymorphic.


### cdi:function
- **Cardinality:** Optional, Repeatable
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** Immutable characteristic of the variable such as geographic designator, weight, temporal designation, etc. (InstanceVariable.function).


### cdi:platformType
- **Cardinality:** Optional
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** The application or technical system context in which the variable has been realized -- typically a statistical processing package or processing environment (InstanceVariable.platformType).


### cdi:source
- **Cardinality:** Optional
- **JSON:** [object reference](#object-reference) or string
- **Description:** Reference capturing provenance information for this InstanceVariable (InstanceVariable.source).


### cdi:hasIntendedDataType
- **Cardinality:** Optional
- **JSON:** [xsdDataType](#sec-xsddatatype), [DefinedTerm](#sec-definedterm), or [skos:Concept](#sec-skosconcept)
- **Description:** The data type intended to be used by this variable, independent of its physical representation (RepresentedVariable.hasIntendedDataType). Recommended values are XML Schema datatypes; see [xsdDataType](#sec-xsddatatype).


### cdi:describedUnitOfMeasure
- **Cardinality:** Optional
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** The unit in which the data values are measured, expressed as a controlled-vocabulary entry (RepresentedVariable.describedUnitOfMeasure). For a plain-string unit, use `cdif:simpleUnitOfMeasure` instead.


### cdi:takesSentinelValuesFrom
- **Cardinality:** Optional, Repeatable
- **JSON:** [cdif:SentinelValueDomain](#sec-cdifsentinelvaluedomain) inline, or [object reference](#object-reference) (`@id` only)
- **Description:** Sentinel (missing / not-applicable) value domain(s) for this variable (RepresentedVariable.takesSentinelValuesFrom). The value MUST be a `cdif:SentinelValueDomain` node — referencing a `cdif:SubstantiveValueDomain` here is a schema violation. Added at the Data Description profile level; not present at the Discovery level; disallowed at the Data Structure level (where the property lives on the RepresentedVariable instead).


### cdi:takesSubstantiveValuesFrom
- **Cardinality:** Optional
- **JSON:** [cdif:SubstantiveValueDomain](#sec-cdifsubstantivevaluedomain) inline, or [object reference](#object-reference) (`@id` only)
- **Description:** The substantive value domain for this variable -- the set of valid, meaningful values (RepresentedVariable.takesSubstantiveValuesFrom). The value MUST be a `cdif:SubstantiveValueDomain` node — referencing a `cdif:SentinelValueDomain` here is a schema violation. Added at the Data Description profile level; same profile rules as `cdi:takesSentinelValuesFrom` above.


### cdi:qualifies
- **Cardinality:** Optional
- **JSON:** [object reference](#object-reference)
- **Description:** Reference to another InstanceVariable in this dataset that this variable qualifies (provides additional context for; e.g. a measurement-channel attribute qualifying a measure variable).


(sec-cdifphysicalmapping)=
## class--cdif:PhysicalMapping
Defines the physical realization of one field in a tabular or structured dataset distribution — the column index (for tabular), the locator (for structured/hierarchical formats like NetCDF/HDF5), the physical type, format pattern, length, null sequence, defaults, etc., and a `cdif:formats_InstanceVariable` reference linking the column or path back to the `cdi:InstanceVariable` it realises in the parent dataset's `schema:variableMeasured`. Each item in a distribution's `cdif:hasPhysicalMapping` array is one CdifPhysicalMapping node. When a WebAPI distribution's `schema:potentialAction/schema:result` carries `cdif:hasPhysicalMapping`, the same shape applies to the response columns and the same `@id`s are referenced (a WebAPI response is another physical realization of the same conceptual variables; do not redeclare the InstanceVariables themselves on the result).

### cdif:index
- **Cardinality:** Optional (required for tabular text)
- **JSON:** integer (≥ 0)
- **Description:** Non-negative integer that orders the fields in the data structure (column number, 0-based). Required for `cdi:TabularTextDataSet`; for `cdi:StructuredDataSet` use `cdi:locator` instead.


### cdi:locator
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Path to the field inside a structured (hierarchical) physical container — for example a NetCDF/HDF5 group path like `/measurements/intensity`, a JSON Pointer, or a Zarr array path. Used in place of `cdif:index` for `cdi:StructuredDataSet` distributions where column-order positioning does not apply.


### cdif:format
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Format pattern for the field — for numbers a token like `decimal`, `scientific`, `integer`; for dates a pattern such as `YYYY/MM` or `YYYY-MM-DDTHH:mm:ssZ`; for booleans the literal token(s) used; etc.


### cdi:numberPattern
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Number format pattern for the field (PhysicalMapping.numberPattern). Text-format properties (column width, decimal/digit-group separators, display label) live on the text-mapping shape below.


### cdif:physicalDataType
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Name of the physical data type for the field as it appears in the file (e.g., `float64`, `int32`, `string`, `dateTime`). Distinct from `cdi:hasIntendedDataType` on the InstanceVariable, which is the conceptual data type.


### cdif:formats_InstanceVariable
- **Cardinality:** Required (Warning if absent)
- **JSON:** [object reference](#object-reference) (`@id` to a `schema:variableMeasured` item on the parent Dataset)
- **Description:** Links this column / path back to the `cdi:InstanceVariable` it physically realises. The `@id` MUST match the `@id` of an item in the parent dataset's `schema:variableMeasured`. SHACL warns if missing (the link is what makes the mapping useful).


### cdi:length
- **Cardinality:** Optional
- **JSON:** integer
- **Description:** Column width for fixed-width tabular text (text-mapping shape).


### cdi:defaultDecimalSeparator
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Decimal separator used when not otherwise specified (text-mapping shape; TextMapping.defaultDecimalSeparator).


### cdi:defaultDigitGroupSeparator
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Digit-group (thousands) separator (text-mapping shape; TextMapping.defaultDigitGroupSeparator).


### cdif:displayLabel
- **Cardinality:** Optional, Repeatable
- **JSON:** string
- **Description:** Human-readable label(s) for display of this field (text-mapping shape; CDIF plain-string simplification of DDI-CDI TextMapping.displayLabel).


### cdi:nullSequence
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Literal token that represents a null/missing value for this field (e.g., `NA`, `-9999`, empty string). Becomes the null annotation for the described column.


### cdi:defaultValue
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Default value substituted when the field is empty.


### cdi:scale
- **Cardinality:** Optional
- **JSON:** integer
- **Description:** Scale factor to apply to stored values to recover the conceptual value.


### cdi:decimalPositions
- **Cardinality:** Optional
- **JSON:** integer
- **Description:** Number of decimal positions (digits after the decimal separator) used to encode the value.


### cdi:minimumLength, cdi:maximumLength
- **Cardinality:** Optional
- **JSON:** integer
- **Description:** Bounds on the textual length of values for this field.


### cdi:isRequired
- **Cardinality:** Optional, default `false`
- **JSON:** boolean
- **Description:** Whether a non-null value MUST be present in each row for this field.


(sec-cdifsubstantivevaluedomain)=
## class--cdif:SubstantiveValueDomain
The set of valid, meaningful values an InstanceVariable can take — distinct from sentinel (missing/not-applicable) codes, which live on a sibling `cdif:SentinelValueDomain`. Used as the value of `cdi:takesSubstantiveValuesFrom`. A single SubstantiveValueDomain node provides EITHER `cdif:takesValuesFrom` (an enumerated list of allowed values) OR `cdif:recommendedDataType` (one or more XSD data type tokens), or both.

### \@type
- **Cardinality:** Required
- **JSON:** string.uri array, MUST contain `cdif:SubstantiveValueDomain`


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this SubstantiveValueDomain node, used when the same domain is referenced from multiple InstanceVariables.


### cdif:takesValuesFrom
- **Cardinality:** Optional
- **JSON:** [cdif:EnumerationDomain](#sec-cdifenumerationdomain) inline, or [object reference](#object-reference)
- **Description:** Enumerated list of allowed substantive values. Use when the value set is a closed vocabulary; combine with `cdif:recommendedDataType` to additionally constrain the data type.


### cdif:displayLabel
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Human-readable label for the domain (e.g., shown in UI).


### cdif:recommendedDataType
- **Cardinality:** Optional, Repeatable
- **JSON:** [xsdDataType](#sec-xsddatatype)
- **Description:** One or more XSD data type tokens recommended for values from this domain. Required if `cdif:takesValuesFrom` is not provided; the SubstantiveValueDomain node MUST carry at least one of `cdif:takesValuesFrom` or `cdif:recommendedDataType`.


### cdi:isDescribedBy
- **Cardinality:** Optional
- **JSON:** [cdi:ValueAndConceptDescription](#sec-valueandconceptdescription) inline, or [object reference](#object-reference)
- **Description:** A `cdi:ValueAndConceptDescription` giving the formal description (value ranges, format/number pattern, regular expression, classification level, logical expression) of the values this domain admits.


(sec-cdifsentinelvaluedomain)=
## class--cdif:SentinelValueDomain
The set of sentinel (missing / not-applicable / refusal / etc.) codes for an InstanceVariable, distinct from the substantive values the variable takes. Used as the value of `cdi:takesSentinelValuesFrom`. Same shape as `cdif:SubstantiveValueDomain` but typed `cdif:SentinelValueDomain` and intended for the non-substantive value codes (so survey "Don't know" / "Refused" codes, sensor `-9999`-style fill values, etc. are represented separately from valid measurements).

### \@type
- **Cardinality:** Required
- **JSON:** string.uri array, MUST contain `cdif:SentinelValueDomain`


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri


### cdif:takesValuesFrom
- **Cardinality:** Optional
- **JSON:** [cdif:EnumerationDomain](#sec-cdifenumerationdomain) inline, or [object reference](#object-reference)
- **Description:** Enumerated list of sentinel codes (e.g., a SKOS concept scheme of missing-value codes).


### cdif:displayLabel
- **Cardinality:** Optional
- **JSON:** string


### cdif:recommendedDataType
- **Cardinality:** Optional, Repeatable
- **JSON:** [xsdDataType](#sec-xsddatatype)
- **Description:** Same semantics as on `cdif:SubstantiveValueDomain`. At least one of `cdif:takesValuesFrom` or `cdif:recommendedDataType` MUST be present.


### cdi:isDescribedBy
- **Cardinality:** Optional
- **JSON:** [cdi:ValueAndConceptDescription](#sec-valueandconceptdescription) inline, or [object reference](#object-reference)
- **Description:** Same semantics as on `cdif:SubstantiveValueDomain`: a `cdi:ValueAndConceptDescription` giving the formal description of the sentinel values this domain admits.


(sec-valueandconceptdescription)=
## class--cdi:ValueAndConceptDescription
A formal description of a set of values — value ranges, format / number patterns, regular expressions, classification level, and logical expressions. Used as the value of `cdi:isDescribedBy` on a `cdif:SubstantiveValueDomain` or `cdif:SentinelValueDomain` to constrain or describe the admissible values beyond (or instead of) an enumerated list.

### \@type
- **Cardinality:** Required
- **JSON:** string.uri array, MUST contain `cdi:ValueAndConceptDescription`


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this ValueAndConceptDescription node.


### cdi:classificationLevel
- **Cardinality:** Optional
- **JSON:** string (one of `Continuous`, `Interval`, `Nominal`, `Ordinal`, `Ratio`)
- **Description:** The measurement/relationship type of the representation: nominal, ordinal, interval, ratio, or continuous.


### cdi:description
- **Cardinality:** Optional
- **JSON:** string
- **Description:** A formal description of the set of values in human-readable language.


### cdi:identifier
- **Cardinality:** Optional
- **JSON:** [Identifier](#sec-propertyvalue-id)
- **Description:** Identifier for objects requiring short- or long-lasting referencing and management.


### cdi:formatPattern
- **Cardinality:** Optional
- **JSON:** [skos:Concept](#sec-skosconcept)
- **Description:** A number/date format pattern as described in Unicode LDML (e.g. `#,##0.###` for a decimal number, or `yyyy.MM.dd G 'at' HH:mm:ss zzz` for a datetime).


### cdi:logicalExpression
- **Cardinality:** Optional
- **JSON:** [skos:Concept](#sec-skosconcept)
- **Description:** A logical expression whose satisfying values are the members of the valid value set (e.g. "all reals x such that x > 0").


### cdi:regularExpression
- **Cardinality:** Optional
- **JSON:** string
- **Description:** A regular expression; strings matching it belong to the set of valid values.


### cdi:minimumValueInclusive, cdi:minimumValueExclusive
- **Cardinality:** Optional
- **JSON:** string
- **Description:** The minimum valid value, inclusive or exclusive respectively (per the W3C Tabular Data Metadata `minimum` / `minExclusive` annotations).


### cdi:maximumValueInclusive, cdi:maximumValueExclusive
- **Cardinality:** Optional
- **JSON:** string
- **Description:** The maximum valid value, inclusive or exclusive respectively (per the W3C Tabular Data Metadata `maximum` / `maxExclusive` annotations).


(sec-cdifenumerationdomain)=
## class--cdif:EnumerationDomain

A codification vocabulary documented as an enumerated value domain — typically a SKOS ConceptScheme listing the allowed values for a `cdif:SubstantiveValueDomain` or `cdif:SentinelValueDomain`. Provides a named extension point so that an EnumerationDomain can either declare an external concept scheme via `cdif:references` or be defined inline.

### \@type
- **Cardinality:** Required
- **JSON:** string.uri array, MUST contain `cdif:EnumerationDomain`


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri


### cdif:identifier
- **Cardinality:** Optional
- **JSON:** [Identifier](#sec-propertyvalue-id)
- **Description:** Identifier for this enumerated (categorical) domain.


### schema:name
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Human-understandable name (linguistic signifier, word, phrase, or mnemonic) for the domain.


### cdif:references
- **Cardinality:** Optional
- **JSON:** SKOS ConceptScheme inline, or [object reference](#object-reference)
- **Description:** SKOS concept scheme that contains the concepts defining the allowed values of this enumeration domain. Reference an external published vocabulary, or inline one. See [skos:Concept](#sec-skosconcept) for individual concept entries.


### cdif:purpose
- **Cardinality:** Optional
- **JSON:** string
- **Description:** Intent or reason for the enumeration domain (or for the description of the object).


(sec-cdifkey)=
## class--cdif:Key
The CDIF profile of DDI-CDI PrimaryKey: an ordered set of `cdi:InstanceVariable` references that uniquely identify a data instance. Used as the value of [cdif:hasPrimaryKey](#cdifhasprimarykey) on the root Dataset. Each variable's position in the key is recorded with an explicit `cdi:ComponentPosition` wrapper carrying `cdi:indexes` (the variable) and `cdi:value` (the integer position), matching the canonical DDI-CDI PrimaryKey structure defined in `ddi-cdif-data-structure`.

### \@type
- **Cardinality:** Required -- `cdif:Key`, Repeatable
- **JSON:** string.uri
- **Description:** MUST include `cdif:Key`.


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this Key node.


### cdif:isComposedOf
- **Cardinality:** Required, Repeatable
- **JSON:** Array of [cdi:ComponentPosition](#sec-cdicomponentposition) wrappers
- **Description:** Ordered list of `cdi:ComponentPosition` wrappers, one per key component. Each wrapper holds `cdi:indexes` (the `cdi:InstanceVariable` at that position -- inline `cdifInstanceVariable` or `@id`-reference) and `cdi:value` (the integer position, 0- or 1-based).


(sec-cdicomponentposition)=
## class--cdi:ComponentPosition
Indexes a single component within a `cdif:Key` (or other ordered DDI-CDI component structure). Used as the items of `cdif:isComposedOf` on a [cdif:Key](#sec-cdifkey): each wrapper pairs an InstanceVariable with its position number in the key.

### \@type
- **Cardinality:** Required -- 'cdi:ComponentPosition', Repeatable
- **JSON:** string.uri
- **Description:** MUST include `cdi:ComponentPosition`.


### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this ComponentPosition node.


### cdi:indexes
- **Cardinality:** Required
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** Reference to the `cdi:InstanceVariable` at this position. Either an inline `cdifInstanceVariable` node or an `@id`-reference to one declared elsewhere (typically in `schema:variableMeasured`).


### cdi:value
- **Cardinality:** Required
- **JSON:** integer
- **Description:** Integer position of this component in the key, incrementing from 0 or 1.


(sec-cdifstatisticscollection)=
## class--cdif:StatisticsCollection
Groups one or more `cdi:Statistics` nodes. A typical use is a dataset-level collection holding row-count / mean / stddev Statistics for each measured variable. Referenced from a CdifInstanceVariable via `cdif:isDescribedBy_StatisticsCollection`, or from the root Dataset via `cdif:statistics`.

### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this StatisticsCollection node.


### \@type
- **Cardinality:** Required -- 'cdif:StatisticsCollection', Repeatable
- **JSON:** string.uri
- **Description:** MUST include `cdif:StatisticsCollection`.


### cdif:has_Statistics
- **Cardinality:** Required, Repeatable
- **JSON:** [cdi:Statistics](#sec-cdistatistics) or [object reference](#object-reference)
- **Description:** Statistics nodes carried by this collection (inline or `@id`-ref). `cdif:` namespaced and target-suffixed because the DDI-CDI `cdi:has` association is polymorphic.


### cdi:hasWeight
- **Cardinality:** Optional
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** The InstanceVariable whose values were used as weights when computing the statistics in this collection.


### cdif:indexedBy
- **Cardinality:** Optional, Repeatable
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** CDIF addition (not in canonical DDI-CDI): the InstanceVariable(s) the contained Statistics index -- the collection-level coordinate space.


(sec-cdistatistics)=
## class--cdi:Statistics
A named bundle of one or more Statistic value objects for an instance variable, optionally weighted, optionally broken down by Category.

### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this Statistics node.


### \@type
- **Cardinality:** Required -- 'cdi:Statistics', Repeatable
- **JSON:** string.uri
- **Description:** MUST include `cdi:Statistics`.


### cdi:statistic
- **Cardinality:** Required, Repeatable
- **JSON:** Array of Statistic value objects
- **Description:** Ordered list of Statistic value objects carried by this bundle. Order is significant -- consumers MAY rely on array position.


### cdi:typeOfStatistic
- **Cardinality:** Optional
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** Controlled-vocabulary entry naming the kind of statistic -- e.g. mean, median, count, sum, stdDev.


### cdi:hasWeight
- **Cardinality:** Optional
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** The InstanceVariable whose values were used as weights when computing the Statistic entries.


### cdif:appliesTo
- **Cardinality:** Optional, Repeatable
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** CDIF addition (not in canonical DDI-CDI): the InstanceVariable(s) this Statistics bundle summarizes -- the per-bundle "what these numbers describe" link.


### cdif:has_CategoryStatistics
- **Cardinality:** Optional, Repeatable
- **JSON:** [cdi:CategoryStatistics](#sec-cdicategorystatistics)
- **Description:** CategoryStatistics entries breaking this Statistics bundle down by Category. `cdif:` namespaced and target-suffixed because the DDI-CDI `cdi:has` association is polymorphic.


(sec-cdicategorystatistics)=
## class--cdi:CategoryStatistics
Statistics for a specific Category of an instance variable within a dataset.

### \@id
- **Cardinality:** Optional
- **JSON:** string.uri
- **Description:** Identifier for this CategoryStatistics node.


### \@type
- **Cardinality:** Required -- 'cdi:CategoryStatistics', Repeatable
- **JSON:** string.uri
- **Description:** MUST include `cdi:CategoryStatistics`.


### cdi:for
- **Cardinality:** Required
- **JSON:** `cdi:Category` node (a concept-like node typed `cdi:Category`, carrying `cdif:name`/`cdif:definition`/`cdif:displayLabel`/`cdif:descriptiveText`), or [object reference](#object-reference)
- **Description:** The Category this CategoryStatistics is for (inline `cdi:Category` node or an `@id`-reference).


### cdi:statistic
- **Cardinality:** Required, Repeatable
- **JSON:** Array of Statistic value objects
- **Description:** Per-category Statistic value objects.


### cdi:typeOfStatistic
- **Cardinality:** Optional
- **JSON:** [DefinedTerm](#sec-definedterm), [skos:Concept](#sec-skosconcept), or string
- **Description:** Controlled-vocabulary entry naming the kind of statistic.


### cdi:hasWeight
- **Cardinality:** Optional
- **JSON:** [CdifInstanceVariable](#sec-cdifinstancevariable) or [object reference](#object-reference)
- **Description:** The InstanceVariable whose values were used as weights.


## Notes

Shared encoding patterns such as [object reference](#object-reference), [DefinedTerm](#sec-definedterm), and [PropertyValue](#sec-propertyvalue-id) are defined on the [Common data types](datatypes.md) page.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_description/dataintegrationintro.md

# Data Integration

Data integration is a task performed on multiple datasets to produce a single unified data set that can be used in analysis.  In a FAIR scenario the requirements and purpose of future data users is not known, and they make decisions about how to integrate the data they are working with. To document such integrated datasets, the fashion in which the data have been integrated from various sources needs to be described, and the process steps recorded. This might include a detailed description of the processing and transformations performed, along with information about the methods, etc, and this crosses into what is typically considered ‘provenance’ metadata. In CDIF, documentation of data integration workflows will be addressed in the context and provenance profile. In the data description and data structure profiles, we are concerned with providing the input information necessary to support those data integration workflows.

This discussion is focused on data that can be represented in tabular formats with simple literal values. Much of the data made available for reuse is expressed in CSV or similar, text-based formats, and these provide the initial focus for describing data, intended as a useful starting point. The profile also addresses widely used array-focused data formats like NetCDF and HDF.

The general intention is that CDIF metadata provides information to enable integrating data across domain and infrastructure boundaries with an acceptable degree of effort, in some cases automated completely. This metadata needs to provide a description of the data types, controlled vocabularies which provide the semantics, and codes used individual fields in the data, possibly supplemented with separate expressions of mapping between controlled vocabularies used. Given this granular description of the data, it is possible to describe the mappings used to merge data sets to enable automation of data integration functions and reduce the high cost of ‘data wrangling’. While it is likely that data integration will always require some attention and input from the researcher, many of the necessary tasks are routine and can be automated if sufficient information is known about the data themselves. CDIF attempts to provide a sufficient level of metadata to support such automation. 



---
### Source Document: data_description/dataintegrationstandards.md

# Standards for Data Description

Many domain-specific standards have excellent descriptions of the data used within their domains, and some of these separate the semantic aspects of data description from the structural ones . [CSV on the Web](https://csvw.org/) is one candidate, as is the [W3C’s Model for Tabular Data and Metadata on the Web](https://www.w3.org/TR/tabular-data-model/). [Frictionless Data](https://framework.frictionlessdata.io/docs/guides/describing-data.html) provides a similar lightweight description of data. More metadata-rich models also exist, such as the [SDMX](https://sdmx.org/) Information Model and the [RDF DataCube Vocabulary](https://www.w3.org/TR/vocab-data-cube/) which is based on it, but these are largely limited to describing multi-dimensional data. Although the [DDI Codebook](https://ddialliance.org/Specification/DDI-Codebook/2.5/) and [DDI Lifecycle](https://ddialliance.org/Specification/DDI-Lifecycle/3.3/) specifications are very close to the CDIF requirements, they are also inherently bound to their intended use for describing social, behavioural, and economic (SBE) data. Only the related [DDI Cross-Domain Integration (DDI-CDI) specification](https://ddialliance.org/Specification/ddi-cdi) meets all of these requirements, largely because it was designed specifically to describe cross-domain data for the purposes of integration.

CSV on the Web is designed to add metadata to CSV tables, which is a use case not dissimilar to the one we address in CDIF. The problems arise when we consider the flexibility of the CSV format itself: there are no limitations in CSV regarding the logical organisation of the contents of the table: is each row a unit being observed, and each column a characteristic of that unit? Or are the columns instead the units? This logical certainty is required. Although CSV on the Web allows us to add richness to the meanings of columns and rows of a table, it is in this sense too flexible to make a good foundation for the scenario addressed by CDIF. We can know what concepts are in play, and how rows and columns are organised, but we cannot understand how the presentation of the data — the table organisation — is logically structured. What roles do the concepts play? While this could perhaps be reverse-engineered, it is easier to explicitly state how the concepts logically relate, and how these in turn are presented in a tabular form. A similar critique can be applied to Frictionless Data’s data description, and to the Model for Tabular Data and Metadata on the Web. These specifications fail to cover all the needed logical relationships, being restricted to tabular descriptions that combine logical and presentational aspects of the data. 

SDMX and the RDF DataCube Vocabulary have a different issue. They have stronger formal models for how concepts intersect with data structure, and do not combine the presentational and logical aspects of data description in the same way, but they are limited because they insist on a multi-dimensional description of data sets. While SDMX 3.0 has introduced a ‘microdata’ description feature, this is still new, and is not yet the version adopted by most implementations, nor is it the version that is the basis for the RDF DataCube Vocabulary.

SDMX demands that the metadata description be provided using a model that might not be supported by disseminator’s systems. Many data repositories do not manipulate data as multi-dimensional cubes, and lack the information needed to describe their data in this fashion. Further, SDMX uses a very disciplined cube definition: all data has regular dimensionality. Many systems based on multi-dimensional models have irregular dimensionality and ‘sub-cubes’, which are not permitted in SDMX. Given that SDMX is an exchange model for official statistics, this disciplined approach is very reasonable, but is not appropriate for CDIF, where existing data stores must be described according to metadata that already exists.

Both DDI Codebook and DDI Lifecycle are excellent models in terms of being generic-but-concept-rich data descriptions, but they lack the range of support needed for CDIF. In the SBE realm, data is overwhelmingly stored and processed as ‘wide’ data files: unit record data, where each record is a set of measurements or values about a single unit, one per row. 

The DDI Cross-Domain Integration specification was developed exactly because it is increasingly common for other types of data to be combined in research projects with this traditional form of SBE data. Four different data structure types are identified: wide, long, multi-dimensional, and key-value (the kind of data commonly found in ‘big data’ systems). Because they are described in a single model, intended to support transformations between these different structural types, the needed separation of logical and presentational aspects of the data was a necessity. DDI-CDI might seem to be a complex model but experience has shown that attempts to produce simpler models based on existing W3C specifications produce equal complexity,  effectively becoming new specifications in and of themselves. The framework recommends DDI-CDI specification for data description as the right approach for CDIF.

Moving forward, there will be more attention paid to the issues of describing data in a way that connects the structural (logical and physical) and semantic description of data more completely. One place where this is likey to happen is in the W3C's [Dataset Exchange Working Group](https://www.w3.org/2026/04/dx-wg-charter.html). Notable here are several existing vocabularies (e.g., DCAT, DataCube) and the new VVD work.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_description/datastructureprofile.md

# Data Structure Profile

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/cdifDataStructureStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructureImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/dataStructureRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructure-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataStructure/index.html)

This profile is focused on the definition of a physical or logical dataset structure in a way that can be packaged and reused for documenting different datasets that have the same structure, for instance periodically released statistics reported in the same format. 

This profile adds DDI-CDI properties for describing a data structure in terms of DataStructureComponents and RepresentedVariables, primary and foreign keys, and mapping of components to their positions in a physical dataset. Value domains for variables are specified in the same way as in the Data Description profile. It has schema for Wide, Long and Dimensional datastructures. The implementation target is an rdf serialization, which is an open world logical model; users are thus free to add additional properties that they find useful for dataset documentation in their community, but these can be ignored by other users without penalty.

Requirements:

- define data structure components
- define represented variables used by each data structure components
- define or identify value domains for each represented variables
- when a reusable DataStructure is used in a dataset description, the represented variables must be mapped to instance variables.

TBD a DataStructure class that defines the file format mappings for the data structure components in a physical implemenation; The only things that the InstanceVariables can modify in datasets using the resusable DataStructure are the labels for the variables and the physicalDataType. 

See [graphical presentation of Data Structure Profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataStructure/index.html)

## Implementation

The current recommended implementation uses the schema.org vocabulary, with a few entities and properties from other vocabularies to fill gaps; see [Implementation of metadata content items](dataStructureSchemaImplementationNew.md). For background on JSON, JSON-LD and general implementation patters CDIF is using, see [Schema.org implementation notes](schemaOrgImplementationpatterns.md).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: data_structure/ddidescriptiondatastructure.md

# DDI-CDI description of Data Structure 
A Data Set has a fixed structure. A data set might be the result of querying services, with the Data Structure generated when the query is executed along with the resulting data. There are three types of Data Set: Wide, Long, and Dimensional. The descriptions of these are very similar, differing mainly in the way they identify specific data cells. Variables are described separately from the Data Structure, because variables can be re-used across different structures. For instance, a ‘Nation’ variable represented with a two-character ISO Country Code might be reused across several different data sets, for example SDG Indicators and the Minimum Set of Gender Indicators. 

The role of a variable within a specific Data Structure is represented by the cdi:Component class. There are several specific types of Components: identifiers, measures, attributes, and so on. These are described as appropriate for each of the three types of data structure. A Component is the specific role played by a variable in the context of a data structure. Each Component appearing in a Data Structure is specific to that Data Structure, and should have its own identity. The variables are the reusable form of the information that can be used across different structures.

## Wide Data Structures

Most data sets can be described as Wide Data Sets in DDI-CDI – these are those cases where each row in a tabular view of the data is a record, and each column is a single variable. To describe a Wide Data Structure, each variable (here we use Instance Variables, acting in their capacity as Represented Variables) is assigned as defining a specific type of Component. In Wide Data Structures, the only Component classes we need are Identifier Components (cdi:IdentifierComponent), Measure Components (cdi:MeasureComponent), and Attribute Components (cdi:AttributeComponent). The diagram below shows how these and other classes are related.

![Wide data structures](./figures/widedatastructures.jpg)

Figure. Wide data structures.

Measure Components hold the observed or measured values in our data. Identifier Components hold specific identifiers assigned to the cases in our data: each record is about a single ‘case’, and these are sometimes assigned identifiers to distinguish them. As in the example provided below, this could be a tax-payer ID for a person, for example, or might be a randomly assigned number in the case where the cases have been anonymised to protect their identities.

```{image} ./figures/widedataexample.jpg
:alt: Long data structure
:class: bg-primary mb-1
:width: 300px
:align: center
```
Figure. Example wide data. TaxpayerID is an identifier component, Taxes Paid is the measure component, and Year is an attribute component.
<br>

It is sometimes the case that an identifier Component is sufficient to disambiguate all the records in the data set: Identifier indicating the row/case, and the variable telling you which value in that record. Often, however, there will be additional fields which are needed (like a timestamp, if the same case was measured/observed on more than one occasion). Attribute Components contain additional information about the measurements/observations which are applicable to each case. Typical Attribute Components are time stamps, geographical coordinates, statuses, or other data related to the context of the measurement or observation. The Primary Key is the set of Components needed to uniquely identify each record in the data set. It is not typically the case that the Measure Components form part of the Primary Key.

## Long Data Structures
If a Measure Component in a data set cannot be clearly associated with a single variable, but relies on the value of another variable to indicate which variable it measures, then you have a Long Data Set, and not a Wide one.   Long Data Sets use additional Components, as they have a more complex relationship to logical variables. An example is useful illustrate the difference between Wide and Long Data Sets. 

```{image} ./figures/longdatasetexample.jpg
:alt: Long data structure
:class: bg-primary mb-1
:width: 400px
:align: center
```
Figure. Long dataset example.
<br>

To describe a Long Data Structure define the logical variables so that each variable has a clear definition, containing a single type of measurement. In this example, the logical variables are Patient ID, Pulse, Weight, Temperature.  These become Instance Variables in the metadata.   The actual columns in the table are considered Presentational Variables, these are Test, Reading, and UoM. 

 In the example table above, the presentation consists of an Identifier Component (*Patient ID*), a column giving us the test performed (*Test*), a column with a measurement (*Reading*), and a column with a unit of measure for the reading (*UoM*). The *UoM* column is an Attribute Component: each entry provides a value that represents a Unit of Measure, and we can easily describe a 'Unit of Measure' variable. The *Reading* column is more problematic: each cell contains a measurement, but they are different types of measures. In order to understand the measurement, you have to consult the *Test* column, which tells you whether it is a pulse, a temperature, or a weight. *This dependency is the characteristic feature of Long Data Sets*.

*Test* is a Descriptor Variable (cdi:DescriptorVariable), and *Reading* becomes a Reference Variable (cdi:ReferenceVariable). A Reference Variable can present measurement values from several logical Instance Variables. The Descriptor and Reference variables together are refered to as a Variable Descriptor Component (cdi:VariableDescriptorComponent) defined by a Descriptor Variable (*Test*), and a Variable Value Component (cdi:VariableValueComponent), which is defined by a Reference Variable (*Reading*).

The resulting metadata will have descriptions of both the logical (*Patient ID*, Pulse, Weight, Temperature) and presentational (*Test*, *Reading*, *UoM*) variables. The Components in my Long Data Structure would reference the presented variables: *Patient ID* (an Identifier Component), *Test* (a VariableDescriptorComponent), and *Reading* (a VariableValueComponent) but the logical variables in turn would all be referenced from the VariableDescriptorComponent and associated classes, as described below.

VariableDescriptorComponents have a refersTo association with a VariableValueComponent; in this example, *Test* will associate itself with *Reading* in this way.

Descriptor Variables will always take their values from a Descriptor Value Domain (cdi:DescriptorValueDomain). This domain is a set of codes that identify logical Instance Variables. The code in the Descriptor Component indicates which Instance Variable the value provided in the corresponding Reference Variable should be associated with. Thus, in our example above, when the *Test* column has a value of 'Temp', we know that the value in the *Reading* field is a measurement of temperature, associated with the temperature logical variable.

The Primary key in a long data structure is assembled from the presentational variables. In the example above, it is a compound key consisting of *Patient ID* and *Test*.

A Reference Variable has a range that includes all possible values of the variables for which it can hold measures. Thus, Reference Variables are often declared as generic types such as XSD string. The specific types of any value can be determined from the description of the associated Instance Variable (the logical variable) specified by the Descriptor Variable.  Figure 17 shows how these presentational classes are connected.

![Long data structure](./figures/longdatastructure.jpg)
Figure. Long data structures - presentational elements.
<br>

The point of having this additional structural metadata for a Long Data Structure is that by providing logical Instance Variables, we are able to reassemble the values in the data set according to other structural arrangements (typically Wide or Dimensional), and to do so programmatically. Although we could have described the example table as a Wide Data Set, the actual variables in the data could not then be re-arranged or re-used: they would be specific to the structure of the data set they appeared in.

## Dimensional Data Structures

A dimensional data structure can be thought of as a multidimensional array, in which each cell in the array contains a measure value. The axes of the array are indexed by Dimension Components. In a Dimensional Data Structure the Primary Key is made up of Dimension Components. Taken together, these address an individual cell with the multidimensional data array, commonly refered to as a cube. That cell holds a value of the Measure Component. Attribute Components are associated with the Measures at the cell level, not at the level of an entire record. The diagram below shows the set of classes which are needed.


![Multidimensional data structure](./figures/multidimensionaldatastructure.jpg)
Figure. Multidimensional data structure.
<br>

The exception to this is if a ‘cell’ has more than one Measure Component, in which case the set of Measure Components requires further disambiguation. This can be specified by qualifying the Primary Key values with the Measure Component/Variable. It is recommended that only a single Measure Component be used;  cells should, if possible, hold simple values such as a string/code, a date-time, or a number. In some cases — notably in the DataCube Vocabulary from W3C and the SDMX specifications on which it is based — the dimensions in a key are ordered. In DDI-CDI, specifying an order is done using the Component Position (cdi:ComponentPosition) class. 

```{image} ./figures/datacubeexample.jpg
:alt: Long data structure
:class: bg-primary mb-1
:width: 400px
:align: center
```
Figure. Example Dimensional Data: Education Level of Belgian Residents
<br>
The table above provides a simple example of a Dimensional Data Set, and how its structure can be described. In this example, the first four columns act as dimensions for addressing the value given in the last column. There would be five Instance Variables described: Year, Degree, Province, Age, and Percent. The representations of these variables would be enumerated using SKOS Concept Schemes except for Year, which would be an XSD gYear, and the Percent variable, which would have a numeric type. Year, Degree, Province, and Age would all be used to define Dimension Components, which could be indexed using instances of the Component Position class, assigning them a ranking from 1 to 4 (ordered low-to-high). Taken together, these four Dimension Components would form the Primary Key. Percent would be a Measure Component. 

# Describe the physical format of the data

In this initial version of CDIF, we are only describing data that is expressed in a textual format such as a CSV file, fixed-width tabular files, or the query result from a relational system. (This is a limitation which will be addressed moving forward.) Further, the assumption is made that any Data Set uses only one structure for all of its records, and that these are organised in a uniform way. These recommendations pertain to data that can be represented in a tabular data structure, packaged in datasets that consist of a set of records that all have the same set of fields. The figure below shows the classes needed for describing the physical encoding of the data.

![Describing physical data layout](./figures/describephysicallayout.jpg)
Figure. Describing physical layouts.

The Logical Record (cdi:LogicalRecord) references all of the Instance variables used within the Data Set. A Physical Segment Layout (cdi:PhysicalSegementLayout) describes the way in which that Logical Record is expressed in the physical file. It has a set of Value Mappings (cdi:valueMapping) instances and corresponding Value Mapping Position (cdi:ValueMappingPosition) instances, which provide the links between the physical layout and the values of the Instance Variables. Physical Segment Layout instances contain much of the information needed by machines to read the data (i.e., character encodings, delimiters, line-end characters, etc.). Note that the formats relationship between Value Mapping and Instance Variable has been collapsed from what is presented in the DDI-CDI model by omitting the intervening Data Point, as Data Points are not instantiated in this profile.


---
### Source Document: examples/index.md

# Example metadata documents

## Schema.org JSON-LD implementation

[Minimal digital object](./SDO-CDIF-MinimalDigitalObject.json)

[Basic dataset](./SDO-CDIF-BasicDataset.json)

[Creator, Contributor Example](./SDO-CDIF-CreatorContributorExample.json)

[Swedish Data Service](./SDO-CDIF-SwedishDataServiceWind.jsonld)

[Ocean Information Hub (OIH) bouy data](./SDO-CDIF-OIH-BuoySeaSurfaceTemp.json)

[Biodiversity dataset](./SDO-CDIF-IndOBIS28001-30000.jsonld)

[Metadata collection](./SDO-CDIF-MetadataCollection.json)


## DCAT, Turtle implementation

[Test example](./DCAT-CDIF-ttl-basic-exampleSMR.ttl)

[Namur Population age distribution](./DCAT-CDIF-ttl-namur-population-example.ttl)

[ICS Geologic Time scale, 2017-02](./DCAT-CDIF-ttl-d33937-ISCtimeScale2017.ttl)

[Parkes pulsar survey](./DCAT-CDIF-ttl-atnf-P366-2003SEPT.ttl)

## DCAT, JSON-LD implementation

[Basic JSON-LD example](./DCAT-CDIF-jsonld-basic-example.jsonld)

[Nobel prize data](./DCAT-CDIF-jsonld-NobelPrizes.jsonld)

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: future/FAIRMappings.md

# Reusable Mappings as FAIR Resources

It is recognized that transformations to both data and metadata at several levels are a critical part of data integration. The mappings used to inform transformations are a critical aspect of this, being both needed provenance information and also potentially providing a reusable FAIR resource in their own right. There is an RDA group working on [FAIR Mappings](https://mapping-commons.github.io/rda-fair-mappings/use-cases/), and the CDIF WG follows this work and attempts to align with it. Currently, the use of A Simple Standard for Sharing Ontology mappings ([SSSOM](https://mapping-commons.github.io/sssom/dev/)) is seen as a useful standard for the expression of mappings, with the RDF Mapping Language [RML](https://rml.io/specs/rml/) also proving to be of interest, This is an area where more work remains to be done, but will be the subject of a CDIF profile in the not-too-distant future.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: future/FullIntegration.md

# Complete Description of Data Integration

CDIF aims to describe the full process of data integration, although that is not entirely possible with the current profiles. This section provides some additional information regarding how CDIF has approached this topic. In the near term, we are looking at the description of mappings, so that they become a truly FAIR resource. This involves tracking some of the developments in this area within the FAIR community broadly, such as in the RDA [FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/use-cases/).

What we do currently cover in CDIF is the description of data sets and structures, and some further discussion of these topics is presented here. It should be noted that there are some developments within W3C which may impact these recommendations moving forward, notably within the Dataset Exchange Working Group ([DXWG](https://www.w3.org/groups/wg/dx/)). Any further developments should be understood in the context of the considerations presented here. (What is anticipated is alignment between some of the various models discussed.)

Also, as CDIF supports a more complete description of provenance, it becomes possible to fully describe the process of data integration.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: future/additionaldataformats.md

# Additional Data Formats


Additional Data Formats (data formats not fully supported in the initial release, such as [NetCDF](https://en.wikipedia.org/wiki/NetCDF), [Parquet](https://parquet.apache.org/), and [HDF5](https://www.hdfgroup.org/solutions/hdf5/) ).

tbd

---
### Source Document: future/context.md

# Context

The context of data is important in understanding its appropriate use in research, including an understanding of the dependencies between different parts of the data, and the purpose and methods of the scientific experiment which produced it. While there is a strong parallel here with provenance, in CDIF we choose to approach these two aspects of data separately, in part because the standards most commonly used to describe context are different from those describing the historical process which has produced the data. Among the standards which are commonly encountered in FAIR descriptions of context is the Research Data Alliance's [I-ADOPT](https://i-adopt.github.io/). This specification supports the description of a variable within its scientific setting, to support the appropriate use of the corresponding data.

There is also a strong relationship between the description of variable context in I-ADOPT and the description of the structure of variables, as we see in the CDIF Data Description and Data Structure profiles. The overlap between these models has been examined, and as a CDIF profile for context is developed, these two aspects of the metadata will be fully aligned. Examples of the use of I-ADOPT are part of some CDIF implementations under the WorldFAIR+ umbrella, and these will also provide concrete input for the development of a profile.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: future/packaging.md

# Packaging data products

Packaging (the creation of archival and dissemination packages)

tbd

---
### Source Document: future/perspectives-ai.md

# Perspectives on Artificial Intelligence

The pace of change in AI technologies has been rapid, and there are many questions about how traditional data and metadata management approaches will be impacted. Large language models (LLMs) require huge amounts of data for training purposes, and the quantitative data used for research is a significant part of that. Unlike more textual data, however, it is not always directly meaningful - a file full of quantitative measurements may not be useful when taken separately from the metadata which drescribes the measurements. (i.e, "What is in the column labelled 'Signif. Quant.' and how is it defined?" does not fuly explain what the numbers in that column actually are, even if the header is understood to mean "significant quantity", and so on.) 

In order to provide data to LLMs in an optimal way, the needed metadata must be provided in a way which allows them to benefit fully from what is known about the data and provided to human users. In order to do this, ML Commons has developed a specification known as [Croissant ML](https://mlcommons.org/working-groups/data/croissant/). The 1.0 version of the specification did not provide a great deal of descriptive metadata regarding the contents of files, but this has been expanded significantly in version 1.1. Further developments will be reflected in version 1.2. Members of the CDIF WG are also active within the Croissant community, to make sure that the approaches used in providing metadata to LLMs are aligned with those for other FAIR purposes. Consequently, there is a high degree of complimentarity between these initiatives. The goal from the CDIF perspective is to ensure the existence of what we term "Semantic Croissant" - a set of metadata for quantitative data, provided as a rich knowledge graph optimized for consumption by AI agents, based on actionable policies. The goal is to ensure that CDIF will always be capable of providing the basis for the provision of high-quality Croissant metadata for consumption by AI agents.

The emergence of agentic AI as a huge force for change in how data is consumed and used has potentially negative effects for data producers, however, and these must also be considered. When it comes to data access, there is insufficient standardization today to ensure that AI agents have the needed information to behave responsibly with the data they consume. Some data providers have reacted to this by removing their data from the Web altogether, so that it is no longer directly available to any intelligences, human or artificial. The situation is problematic, and can only be solved by having a standard expression of conditions of use and licensing, couched in terms which can be read and understood by both humans and machines. Revision of information must also be accomodated, such that accurate information exists whether what is wanted is an historical picture or the latest, most accurate version. Further, there needs to be some mechanism for enforcement, such that access is practically controlled by the owners and stewards of data. 

Toward this end, the CDIF WG has been exploring how different systems of access, based on ODRL, and other mechanisms can be combined. This has raised interest in the use of Decentralized Identifiers ([DIDs](https://www.w3.org/TR/did-1.0/)). This remains an area of focus.

AI topics go beyond what is discussed here: agentic AI tools can be extremely helpful in the production of needed metadata and documentation, so long as they are applied correctly, and can also play a significant role in harmonization of concepts and the integration and analysis of data. The goal is to have AI-ready data and metadata resources, which are flexible enough to support not only the needs of existing AI, but also those of the future. As it is further developed, CDIF will be looking at how such applications impact the core set of metadata needed for FAIR exchange of data across domains and infrastructures. 


---
### Source Document: future/provenance.md

# Provenance

Describing the provenance of data and other FAIR resources is potentially a very broad topic, including a wide range of metadata of different types. For the purposes of CDIF, we have chosen to limit the topic in the same way that the popular PROV recommendations from W3C deso: "Provenance is information about entities, activities, and people involved in producing a piece of data or thing, which can be used to form assessments about its quality, reliability or trustworthiness." (from the "PROV Overview at [http://www.w3.org/TR/2013/NOTE-prov-overview-20130430/](http://www.w3.org/TR/2013/NOTE-prov-overview-20130430/)). Provenance is a critical topic for the sharing of FAIR resources across domain boundaries, as the knowledge of data and sources may not be as thorough as that of resources from within the domain, and the determination of reliability and trust may be more difficult.

The most important aspect of provenance to record - and the one on which the existing standards focus - is the process whereby data or another resource has been created and processed. There are several popular standards for describing historical processes: the W3C PROV family of recommendations are very popular, but are not so much a single standard model as they are a framework for describing any kind of provenance. They typically require - and are designed for - a degree of specialization to make them relevant within a domain. This has the impact of making PROV descriptions potentially problematic for cross-domain use. Other popular standards which support description of historical process include Schema.org, the Common Workflow Language (CWL), and the process portion of DDI-CDI. For the purposes of CDIF, CWL is not ideal because XML is its only syntax representation, while all the others have at a minimum an RDF vocabulary which can be expressed as JSON-LD, like all of CDIF (DDI-CDI has both standard XML and RDF syntax representations.) In almost all cases, the weakness found with PROV - the need for specialization to have broadly meaningful process descriptions outside a specific domain - was also present with other standards. As a result, it is not practical for CDIF to select a single standard for implementation, and recommend a set of the available fields for implementation of CDIF from it.

The CDIF Working Group has been actively working on provenance for several years, and it is expected that a recommended profile will be forthcoming in the near term. The work has been conducted in a bottom-up fashion, looking at examples of data collection and production across many different domains. From these, a more generic description of typical activities, resources, and actors has been developed. The implementation of this "cross-domain" description of process is potentially possible across several of the mentioned standards, and the idea that the CDIF provenance model will be essentially the same regardless of the standard vocabulary used for describing the historical process (e.g., PROV, Schema.org, or DDI-CDI) is being explored. Further, reference models of data production such as the UN/ECE's [Generic Statistical Business Process Model (GSBPM)](https://unece.org/statistics/gsbpm-v5.2) are being explored in implementation projects which are using CDIF (such as [Climate-Adapt4EOSC](https://climate-adapt4eosc.eu/)).  

Some basic fields for capturing provenance exist within the Discovery profile, taken from the W3C PROV vocabulary, but these are minimal. A more complete set of recommendations regarding provenance can be expected soon the the CDIF WG completes their work on this topic.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: introduction.md

# Introducing CDIF

Version 1.1 June 2, 2026

Many important research questions demand a multi-disciplinary approach in which data and resources are used across domain and infrastructure boundaries. In such scenarios, domain-specific community standards fall short of the requirements for FAIR exchange of the critical metadata and other information needed. The **Cross-Domain Interoperability Framework** (CDIF) is designed to support FAIR implementation for these projects by establishing a ‘lingua franca’ for this information, based on existing standards and technology to support interoperability, in both human- and machine-actionable fashion. CDIF is a set of implementation recommendations, based on profiles of common, domain-neutral metadata standards which are aligned to work together to support core functions required by FAIR.

The idea for CDIF first emerged from workshops and discussions at conferences prior to the WorldFAIR project, beginning in 2018. The WorldFAIR project provided an opportunity to advance that vision, through aset of 11 case studies across many domains, allowing the needs and practices around FAIR within such domains to be summarised in the form of FAIR Implementation Profiles (FIPs). Based on the FIPs and focused meetings, the requirements for CDIF were established. A group of 30 invited experts from different FAIR initiatives and standards bodies made up a Working Group and an Advisory Group to synthesise the findings from WorldFAIR and to produce the current CDIF draft.

The framework is based on a set of profiles that address the most important functions for cross-domain FAIR implementation by providing core metadata fields useful in all domains and infrastructures. Below is a list of the functions and the profiles supporting each of them:

- Discovery, Cataloguing, and Dissemination (Search, indexing, and packaging)
  - Data Discovery Profile (Search, cataloguing, and indexing)
  - Manifest Profile (Packaging of resources for archiving and reuse)

- Data Description, Use, and Integration
  - Data Description Profile (Detailed description of quantitative data)
  - Data Structure Profile (Reusable data structures and essential variables)
  - Codelist Profile (Enumerated values and classifications used in data)
  - Concept Scheme Profile (Glossaries, controlled vocabularies, and other semantic resources)

- Controlling Data Access (Data confidentiality, access, and permitted use)
  - Access Rights Profile
- Core Metadata and Universals (Administration and common expression)
  - Core Profile (Basic fields used in all profiles)
  - Universals Profile (description of ‘universal’ elements – time, geography, and units of measurement across other profiles) for archiving

Under Development:

- Characterizing Data
  - Provenance Profile (Processes producing and editing data)
  - Context Profile (Scientific background of variables)

Each of these profiles is supported by specific recommendations, including the set of metadata fields in specific standards to use, and the method of implementation to be employed for machine-level interoperability.

CDIF is designed to leverage the work of other FAIR initiatives such as FAIR-Impact and the work in EOSC. It is designed to be implementable with existing tools, standards, and technologies but, as a set of recommended practices, must be maintained as FAIR implementations develop and evolution occurs in the technology sphere. CDIF leverages methodologies such as FIPs from the [GO FAIR Foundation](https://www.go-fair.org/how-to-go-fair/fair-implementation-profile/). Importantly, it aligns with efforts such as the [EOSC Interoperability Framework](https://op.europa.eu/en/publication-detail/-/publication/d787ea54-6a87-11eb-aeb5-01aa75ed71a1/language-en), and developments such as [Signposting](https://signposting.org/FAIR/) and reference implementation of the [FAIR Digital Object Framework](https://fairdo.org/). Work on semantic mapping and in some other areas is informed by on-going developments in other fora such as [RDA](https://www.rd-alliance.org/). CDIF is designed to enable the practical implementation of FAIR by supporting these frameworks and approaches in cross-domain scenarios.

In any given domain, the standards used should be to a considerable extent mappable to and from their corresponding CDIF profiles, reducing the volume of mappings needed to interoperate effectively for core FAIR functions in multi-disciplinary scenarios. Broadly speaking, FAIR demands an increase in the metadata provided by the disseminators of data, especially if we are to automate resource-intensive data integration tasks, which today are largely manual. In a cross-domain scenario, the sheer number of mappings needed is not supportable. CDIF provides a solution by changing a many-to-many dynamic into a many-to-one dynamic.

# What is CDIF

**CDIF is not intended to replace existing community standards**, but to supplement them for communication across domain and infrastructure boundaries. It does not aim to replace the specific models needed within different domains, but it does aim to establish a foundation of common metadata which can support a core set of FAIR functionality. Real-world examples of large-scale standards-based exchange networks, such as the [Statistical Data and Metadata Exchange](https://sdmx.org/) (SDMX) and the [Ocean InfoHub](https://oceaninfohub.org/odis/) (ODIS) have been used as inspiration for the overall approach, to ensure its feasibility for practical implementation. This draft includes links to early prototypes for such data as the Sustainable Development Goal Indicators and some of their source data, showing how the mining of the native standard descriptions of the source, to produce its equivalent in CDIF, can support disaggregation and integration of that data with other sources.

There is a wealth of research on how FAIR can be implemented, and investigations into this subject show no sign of abating. CDIF is not a research project, nor does it intend to outline the best possible solution to the challenges of FAIR implementation. Instead, it is first and foremost a practical exercise: how can we find a set of common standards and technology approaches that will enable us to implement FAIR for cross-domain scenarios using things which exist today? Standards are only useful if they are agreed and implemented, so CDIF tries to advocate those standards and technology already in common use. There are gaps in current practice that require additional information and standards, but these are minority cases. Web standards already exist for supporting most of the needed functions, but they are not always used in ways which are interoperable, requiring a common approach for at least some core aspects. The CDIF recommendations are based on practical considerations: we must agree on a body of practice, and whether it is the best possible solution is a secondary concern. More important is that it be implemented widely, so that FAIR exchange can become as easy as possible. Once laid, such a foundation can be perfected.

To this end, CDIF identifies a set of common functions which are needed to implement FAIR: describing data for discovery and assessment, supporting access to data by describing the licensing and conditions of use, laying out the structure and semantics of data to support automated integration, and providing information regarding the provenance of data and resources. In each area, practical recommendations are made regarding what standard or standards should be used, and how they should be implemented. In those areas where there is no clear practice which can be recommended, or which require further investigation, this is noted. For the provision of basic discovery metadata, the description of licence conditions, the publication of controlled vocabularies, and the description of data to make it ‘integration ready’, specific steps are described which can be used to guide immediate implementation.

# Who Can Use the CDIF?

CDIF is aimed primarily at data infrastructures, i.e. those organisations which develop, maintain, and disseminate FAIR resources for reuse, often as centralised points of access within their communities or area(s) of interest. While data stewardship by research organisations is an important element of FAIR, not all research organisations perform this dissemination, instead relying on data archives or other dedicated repositories. FAIR reuse is most effective when authoritative producers, or those acting on their behalf, provide their data and metadata to others for reuse, so the authoritative versions of such resources are the ones which get reused. Such organisations are often motivated to be the point of dissemination, as it is their mission, and they bear the responsibility, both legal and reputational, for those resources. CDIF is a tool which they can use to better support this mission.

# The CDIF Working Group, Advisory Group, and Community

Many people have contributed and we'd like acknowledge their time and effort. CDIF historically has been made up of a Working Group (and sub-groups) and an Advisory Group.

For the immediate future, significant development will take place under the auspices of the [CDIF4EOSC Project](https://cdif4eosc.eu/), in coordination with the CDIF Working Group and Advisory Group.

To apply to join CDIF working or advisory groups, please [use this form](https://forms.gle/bX5sg5pVGfHmecNK9). If you simply want to keep up to date with developments, [please register to join the CDIF community list](https://bit.ly/cdif-community-list).

<!-- cdif-footer-include -->

:::{include} \_static/footer.md
:::


---
### Source Document: manifest/manifest.md

# CDIF Manifest Profile

Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/cdifManifestStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/CDIFManifestImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/manifestRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/cdifManifest-frame.jsonld)
- [Transform RO-CRATE to/from CDIF](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/tree/reviewRevision202606/tools)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFManifest/index.html)

## Overview
Within the set of FAIR functions supported by the CDIF guidelines is a practical need to construct packages of related files that are treated as a single resource. This requirement appears in different forms: Researchers must be able to collect and group the various resources involved in their research, so that sense can be made of it for the purposes of replication, comprehension, and reuse. Archives and repositories have a requirement for packages of related resources to be submitted and stored, and these form the basis for dissemination. There is the popular concept of a FAIR Digital Object (FDO) which can be anything FAIR – even an atomic metadata item – but in practical terms requires that coherent packages be assembled to support practical use.

In a networked scenario, it may not always be the case that every required resource is stored at the same location or is found within the same repository (even a distributed one). In such a case, the idea of a "package" is not so much a physical assembly as it is a list of needed resources and the addresses – local or otherwise – which can be used to retrieve them. Different scenarios of use will impose different restrictions on how such packages need to be stored, but in their most basic form, they are a list of resources and locations: a manifest.

This CDIF recommendation is designed to support documentation of resource packages, the core items which make up a manifest. This document outlines the basic requirement, the conceptual model, and discusses specific implementation using schema.org and RO-Crate.  

## Requirements
1. Support the retrieval of complete packages of related resources sufficient for the FAIR use of a data or metadata object
2. Contain a listing of each component part, along with needed identifiers, descriptors, typing, and charaterization so that both humans and machines can understand its content and relationship to other parts of the package
3. Provide information sufficient to retrieve each of its component parts within the context of the system or network on which it is located. This does not require that the individual parts of the package can be retrieved on the web.
4. Be self-describing so that a receiving system can determine how to process it. Ideally, it will be useable by any application which supports the type of packaging which was used to implement the CDIF model (that is, it will not require a CDIF-aware application to unpack).
5. Identify conformance to the CDIF Manifest profile, so that receiving systems can understand how to operate on it if they support the CDIF profile.

Note that functioning as an FDO is not necessarily a requirement out of the starting gate - that should be added later, once we can figure out what it means. It is not a business requirement.

## Information Model
-	Protocol Conformance Statement (Required) – a statement of the protocol used to constitute the package being described, and to which supplied information conforms (RO Crate, Frictionless Data, etc.)
-	Package identification  (R) – a unique identifier for the package, according to a known scheme
-	Package name (O) – a human-readable name for the package to help distinguish it from others.
-	Package description (O) – a human-readable description of the package and its contents and purpose.
-	Package date (O) – The data of the creation of the package (may include time).
-	Package creator (O) – Information about the creator of the package for the purposes of attribution. May contain contact information.
-	Distribution Information (conditional) – information needed to locate and retrieve the package (unless the metadata is an item inside the package).
-	Item List (R) – A list of the items which are the parts of the package. Each has an ID and a location. These may be local (within the package container) or somewhere on a network, with the provided location information being sufficient for them to be retrieved. 
-   Item type (R) - categorization of kinds of item, typically MIME type, other categories or  semantic classification also allowed (e.g., "data entities," "context entities").
-	Licensing information (R) – according to IP law, assemblages can have different licensing than their constituent parts. The license for the package is required, but more restrictive licenses may be associated with individual resources in the package.

## Implementation
This model can be implemented in different ways – it could be an RO Crate, a Frictionless Data Data Package, a schema.org DataDownload with parts, etc.  There are two main use scenarios:1) a standalone metadata record describes a packaged resource for use by metadata harvesters indexing metadata records for discovery interfaces; 2) The metadata record is included inside a data package for use by applications using the contents of the package. RO-CRATE is focused on the second case, whereas most of the CDIF effort has been in support of the first case. The CDIF data description and data structure profiles provide metadata elements to document the structure of data in individual media object in a package. 

### RO Crate 
RO Crate implementation will conform to the [RO-CRATE 1.2 specification](https://www.researchobject.org/ro-crate/specification/1.2/ro-crate-preview.html). RO-CRATE extensively uses schema.org, and is thus broadly compatible with CDIF. A cdif conformant RO-CRATE must include a CDIF metadata file in the package, and reference that file in the manifest. 

Thus a node like this must be included in the RO-CRATE metadata file:

    {
      "@id": "cdifmetadata.json",
      "@type": "File",
      "name": "CDIF metadata",
      "contentSize": "3866",
      "description": "CDIF formatted file conforming to manifest URI",
      "encodingFormat": "application/JSON-LD",
	  "dcterms:conformsTo":"https://w3id.org/cdif/manifest/1.1"
    },


Some important distinctions include: 
-	 Metadata File Descriptor -- a CreativeWork entity with \@id: "ro-crate-metadata.json" that points to the Root Data Entity via about.
- Serialize as flattened, condensed JSON-LD file. all entities (dataset, files, people, organizations) appear as top-level objects in a flat \@graph array, cross-referenced by \@id. 
-	Document root \@type "schema:CreativeWork" (same as RO Crate 1.2). 
-	Will have "ro-crate-metadata.json" as the graph \@id, and the file will be named "ro-crate-metadata.json" and appear in the root of the package.
-	Data Entities -- File (alias for MediaObject) and Dataset entities representing files and folders.
- Contextual Entities -- Person, Organization, Place, etc. entities referenced from the data entities. These match CDIF core requirements.


schema.org implementation 
- CDIF core covers the basic RO-CRATE metadata	
- Packages delivered as zipped (or similar single-file) archive are considered schema:DataDownload objects.
- indidividual parts of the package are typed as schema:MediaObject (like RO-CRATE); they are not required to have a schema:contentURL property because they're not expected to be individually downloadable.  Other \@Type can be assigned to the package parts, as well as schema:additionalTypes that don't impact the content model for the node, but assist in semantic interpretation. 

# Dataset Properties added by the CDIF Manifest Profile

## schema:Dataset {#sec-schema-dataset}

Profile module for archive distributions. Marks the catalog record as conformant to the CDIF manifest spec (https://w3id.org/cdif/manifest/1.1) and lets schema:distribution items carry schema:hasPart describing the component files inside an archive (ZIP, etc.). The base schema:distribution anyOf [DataDownload, WebAPI] contributed by cdifCore is preserved — this BB only adds property constraints, no new anyOf branch. (Merged from the previous cdifProfile/cdifArchive BB, which held only the $defs for ArchivePart; everything now lives here.)

### schema:subjectOf
- (required) conformance statement in the subjectOf/dcat:catalogRecord must include "dcterms:conformsTo" includes    "https://w3id.org/cdif/manifest/1.1"

### schema:distribution
If the DataDownload type is application/zip (might need more general way to identify bundled packages of files), then the DataDownload must have hasPart properties that are schema:MediaObject instances describing the contained files. 
- **Cardinality:** Optional

# Class Definitions

## MediaObject

### \@type
-  (Required) May include additional types for categorization.  type: array of string, must contain "schema:MediaObject", may not contain "schema:DataDownload" since the media objects in the package are not independently downloadable.
### schema:name":
- (Required) locator for the mediaObject within the package. If Some package components are remote (external to the package) this must be a resolvable locator (e.g. http URI). Type: string
### schema:description
- Description of the file content. Type: string
### schema:encodingFormat
- Type(s) of the media object. type: array of string. MIME type is expected, other classifiers  may be included
### schema:size
- File size as a schema:QuantitativeValue value, with a numeric value and unit of measure: type: schema:QuantitativeValue.
### schema:about
- For metadata sidecar files, references the data file this metadata describes. type: array of object reference to the \@id of the data file described by this sidecar.
### spdx:checksum
- checksum object contains string value calculated algorithmically from the mediaObject content to allow determination if the object has been corrupted. type: spdx:Checksum object.


## schema:QuantitativeValue"
- object that specifies a numeric value and units of measure
### schema:value":
- (required) numeric value. type: number
### schema:unitText":
- Unit of measure for size (e.g. 'byte'). type: string

				
## spdx:Checksum
### spdx:algorithm
- (Required) Name or identifier for the algorithm used to calculate the checksum. type: string
### spdx:checksumValue
- (required) the checksum string. type: string


The formats can be interchanged losslessly, Code for the tranformation is located here:

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/archive/contentmodelbku.md

# Basic discovery metadata content model

The core of the CDIF profile for resource discovery is a set of implementation-independent content requirements that specify the required information to support a basic level of discovery interoperability for resources of any type.  The following list includes the minimum required content for basic resource description, discovery, and access. This recommendation is a synthesis of various metadata schemes, including ISO 19115-1:2014, schema.org conventions from ESIPFed Science on Schema.org and Ocean Data net, DCAT, DCAT-AP, and [FDO Kernel Attributes-2.0](https://docs.google.com/document/d/1OF49wTNVuv-6OXlNerhBTqVtHyc7jutTaUHjn6BZCs0). A mapping between these various schemas and CDIF content elements is available in [TBD](tbd). Note that these content requirements are scoped for a broad spectrum of resource types. It is expected that other fields will need to be added in extensions for specific kinds of resources.

## Required
If the content of a required element does not provide useful information, the metadata is considered useless for even the most rudimentary discovery use cases. Conformant metadata MUST provide valid values, i.e., a meaningful title that identifies the resource, either a URL or text statement of how to obtain the resource, a statement of any licensing, usage, or access constraints (i.e., Rights), and identifiers for the specification of the metadata serialisation and the type of the resource described.

- **Resource identifier** (1 entry): A globally unique, resolvable identifier for the resource described by the metadata record.
- **Title** (1 entry): Succinct (preferably &lt;250 characters) name of the resource; should be sufficient to uniquely identify the resource for a human user.
- **Distribution**: URL, Distribution object, or Access Instructions (1 entry): If the resource is a digital object accessible online, provide a URL that will retrieve the resource. If the resource has multiple representations, provide a Distribution Object documenting the various options with a URL and representation profile for each. Metadata for distributions through an API that allows query, filter, or processing as part of a data access request are described in the Queryable Distribution Interfaces (API) section, below. If the resource is not accessible online, provide a URL to a landing page used to access the resource, or minimally, provide a text description explaining how to access the resource in the metadata (Access Instructions).
- **Rights** (1 to many entry): Information about required access permissions, licences, contractual requirements, use constraints, and security constraints. Might be described in text or through links to external documents. (See 6.4. Data Access for providing machine-actionable rights descriptions.)
- **Metadata profile identifier** (1 to many): Identifier for metadata specification (profile) used to create this metadata record. Generally this will be populated automatically if the metadata is created using CDIF aware tools.
- **Resource type** (1 to many): A scoped name (label with classification scheme) that specifies the kind of resource described by the metadata. The resource type might be used to determine validation requirements specific to descriptions for that kind of resource.

## Required, but nilable
These are content elements for which every resource should have useful information, but for which the information may not be available. A corresponding field should be included in each metadata record, but may have value 'nil:missing', 'nil:unknown' or similar nil value. Use 'nil:notapplicable' for Temporal Coverage, Geographic Extent or Statistical Variable when these are not applicable to the described resource.

- **Description** (1 entry): Inform the reader about the resource's content, context, provenance, and any other information deemed useful for future cross-domain usage.
- **Originators** (1 to many entries): One or more parties (person or organisation) that have a role related to the origin of the resource, e.g., author or editor. Each party has a name (label), identifier, and optional contact information.
- **Modified Date** (1 entry): Date (not temporal extent) when the most recent changes to the resource were completed. Use a "year" or [ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601) format. Alternative date formatting must be machine-readable and consistent across all datasets.
- **Distribution Agent** (1 entry):The party (person or organisation) to contact about accessing the resource. Each party has a name (label), identifier, and optional contact information. If there are multiple distribution options with different contact points, the Distribution Agent should be specified as part of the Distribution Object.
- **Variable** (0 to many entries): Only applicable to datasets. The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be, ideally, qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text. Variable metadata should include as much content as needed for users to understand the type of the variable (e.g. measured, statistically derived, or simulated), its units, and any relevant reference systems for its values (see [Universals](../universals/univintro.md) ). Details of data structure and schema more closely related to interoperability, data integration, and usage than to data discovery are discussed in [tbd](tbd). Describing Data to Make it "Integration-Ready".
- **Temporal Coverage** (1 entry). The time interval represented by or the subject of the described resource. This could be the time interval when data were collected, or an archaeological or geological time interval that is the subject of the resource. Need to account for clock time, calendar time (Gregorian, Julian, Hebrew, Islamic, Chinese, Mayan...), cyclical time (summer, first quarter, mating season, new moon, pay day) and for named time ordinal eras (Jurassic, Younger Dryas, Early Minoan I, Late Stone Age). See [OWL Time](https://www.w3.org/TR/owl-time/).
- **Geographic Extent** - horizontal (if applicable, 1 entry, minimum bounding rectangle or point): In order to support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 8486 datum. There are various other systems for describing location (see [Space](../universals/univgeography.md) ); these can be provided as alternate location descriptions, recognizing that they might be meaningful to some metadata harvesting agents. Some resources may not be usefully described by a WGS 84 extent, in which case indicate nil:notapplicable; this would include extraterrestrial resources.
  - *Bounding Rectangle*: North Bounding Latitude, South Bounding Latitude, East Bounding Longitude, West Bounding Longitude. The minimum rectangle that completely contains the coverage extent for the resource content. Coordinate order and syntax are determined by the serialisation profile.
  - *Point*: Latitude, Longitude. A centroid point for the coverage extent of the resource, or the location of the resource content if a point location is appropriate. Coordinate order and syntax are determined by the serialisation profile.
  - *Named location*: Place name referenced to some gazetteer. Use scoped name pattern {label, authority, optional identifier} (see [placename](tbd) ).
  
## Required for metadata management
These elements provide essential information for the operation of a distributed catalogue system with harvesting of metadata between catalogue servers. Values should be populated automatically by metadata creation tools, requiring no user input. Nil values are allowed.
- **Metadata Date** (1 entry): Last metadata update/creation date-time stamp in ISO 8601 date and time format. This may be automatically updated on metadata import if a metadata format conversion is necessary.
- **Metadata Contact Agent** (1 entry): The party responsible for metadata content and accuracy; Agent object includes a name (label), identifier, and optional contact information
- **Metadata Identifier** (1 entry): The identifier for the Digital object that contains the metadata.

## Recommended
Other properties that should be specified if possible and relevant. All are optional.
- **Checksum**. (0 or 1): A string value calculated from the content of a digital object that allows verification that the content of the object has not been modified. Even insignificant changes to the content of the file will change its checksum. The algorithm used to calculate the checksum must be documented. See also [RFC-6920 'Naming things with hashes'](https://www.rfc-editor.org/rfc/rfc6920.html) that establishes ways to identify checksum algorithms and to represent checksum values as a URI. Note that checksums apply to specific digital objects, typically a unique resource representation. Non-digital resources do not have checksums; their representations can have checksums. See implementation notes in Appendix 1.
- **Funding**. (0 to many entries): Cite funding sources (Grants, contracts...). Each source has a grant or contract identifier, source organisation, and label.
- **Keyword** (0 to many entries): Distinguish 'tags' and 'controlled terms'. Tags are simply words that a metadata creator thinks will be useful for users to identify resources of interest. Controlled terms are words defined in a vocabulary that minimally include the word (a fixed string to identify the term for humans) and a definition. Each term represents some concept. More semantically rich vocabularies would include resolvable identifiers, source information, and links to related terms (see [Cox et al., 2021](https://doi.org/10.1371/journal.pcbi.1009041) ). One common set of relationships in a vocabulary is a kind-of hierarchy linking broader to narrower concepts. Controlled terms should minimally be represented in metadata with a label and scheme name that identifies the source vocabulary; ideally a term URI and scheme URI could be included for more accurate identification and data integration.
- **Policies** (0 to many entries): Policies used in management of the described resource, including whether the content may be changed (mutable or immutable), any scheduled updates, what is the expected lifetime for resource availability, what (if any) is the maintenance schedule, versioning, documentation for changes and change requests. Explicit support for specific policy frameworks can be included (e.g., CARE).
- **Publication Date** (0 or 1): Date (not temporal extent) when the resource was made accessible. Use a ‘year’ or ISO 8601 date and time format. Alternative date formatting must be machine-readable and consistent across all datasets. If no publication date is known, estimate the publication date range, enter the oldest year as the publication date, and include the estimated date range in the Description field.
- **Other related agents** (0 to many entries): Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators. Includes a variety of roles like maintainer, publisher, point of contact, copyright holder, contributor (see e.g. [DataCite contributor types](https://datacite-metadata-schema.readthedocs.io/en/4.5_draft/properties/recommended_optional/property_contributor.html#a-contributortype), [ISO19115-1 role code](https://wiki.esipfed.org/ISO_19115_and_19115-2_CodeList_Dictionaries#CI_RoleCode) )
- **Related resources** (0 to many entries): Links to related data, publications, annotation, data sources, software used, etc. Links have at least a label, relationship type, and resolvable target resource identifier.
- **Version** (0 or 1): If the resource is versioned, specify the label for this version. Version labels should follow a scheme that allows alphanumeric sorting reflecting the order of version release.
- **Provenance** (0..many): For discovery, provide information about datasets that were used in the creation of the described resource and specify sensors, platforms, software, algorithms etc. used to aquire information contained in the resource.  Details about workflows, activity sequences, association of sensors etc. with specific variables, individuals associate with particular activities in workflow etc. require used of cdif prov extension [tbd](./tbd).
- **Quality** (0..many) Provide statements about the quality of information in the described resource,  information about quality policies or certificates that apply to the resource, and results of quality measures with information about the measurement protocol/procedure used. In all cases the focus should be on information useful for initial assessment by potential users.

---
### Source Document: metadata/archive/schemaOrgImplementationTablev2.md

# Implementation of metadata content items

The following table maps the metadata content items described in the [Metadata Content Requirements](./contentmodel.md) section to the schema.org JSON-LD keys to use in metadata serialization. Some example metadata documents follow. The \'Obl.\' column specifies the cardinality obligation for the property; \'1\' means one value required; 1..\* means at least one value is required; 0..\* means the property is optional and more that one value can be provided. Properties with path from "subjectOf" describe the metadata.


<table>
  <tr>
    <th><b>CDIF content item</b></th>
    <th><b>Obl.</b></th>
    <th><b>Schema.org implementation</b></th>
    <th><b>Scope note</b></th>
  </tr>
  <tr>
    <td>Metadata identifier</td>
    <td>1</td>
    <td>"schema:subjectOf"/"@id":{URI}</td>
    <td>The URI for the metadata record should be the \@id value for the 'schema:subjectOf' node. This node has \@type ["schema:Dataset"] with schema:additionalType ["dcat:CatalogRecord"], and a schema:about property referencing the \@id of the root resource node.</td>
  </tr>
  <tr>
    <td>Resource identifier</td>
    <td>1</td>
    <td>"schema:identifier":{PropertyValue or string}</td>
    <td>The primary identifier for the resource. Can be a simple string (ideally a resolvable URI), or a schema:PropertyValue with schema:propertyID (identifier scheme), schema:value (the identifier string), and schema:url (resolvable link). The PropertyValue approach is strongly recommended.</td>
  </tr>
  <tr>
    <td>Title</td>
    <td>1</td>
    <td>"schema:name":{string}</td>
    <td>A set of words that should uniquely identify the described resource for human use, in the scope of the metadata catalog containing this metadata record.</td>
  </tr>
  <tr>
    <td rowspan="2">Distribution</td>
    <td>1</td>
    <td>"schema:url":{URL}</td>
    <td>If metadata is about a single digital object. Either schema:url or schema:distribution (or both) must be present.</td>
  </tr>
  <tr>
    <td></td>
    <td>"schema:distribution": <br> [{ "@type": ["schema:DataDownload"], <br> "schema:contentUrl": {URL}, ... }, <br>{ "@type": ["schema:WebAPI"], ... }]</td>
    <td>An array of distribution objects. Items may be DataDownload (file-based, requires schema:contentUrl) or WebAPI (service-based). The \@type is encoded as an array. DataDownload should include schema:encodingFormat and dcterms:conformsTo.</td>
  </tr>
  <tr>
    <td>Rights</td>
    <td>1..*</td>
    <td>"schema:license":[{text or URI or CreativeWork}, ...] <br> Or <br> "schema:conditionsOfAccess":[{text or URI}, ...]</td>
    <td>At least one of schema:license or schema:conditionsOfAccess must be provided (as arrays). URL to license document or text explanation of restrictions on use.</td>
  </tr>
  <tr>
    <td>Metadata profile identifier</td>
    <td>1..*</td>
    <td>"schema:subjectOf"/"dcterms:conformsTo": <br>[{"@id": "https://w3id.org/cdif/core/1.1/"}, <br>{"@id": "https://w3id.org/cdif/discovery/1.1/"}]</td>
    <td>An array of objects with @id values that are conformance URIs. For CDIFDiscovery, both the core and discovery URIs are required. Extended profiles add their own conformance URIs to this array.</td>
  </tr>
  <tr>
    <td>Metadata date</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:sdDatePublished":{Date}</td>
    <td>Use ISO8601 format. The most recent publication date for the metadata content. Harvesters use this to determine if they have already harvested and processed this record.</td>
  </tr>
  <tr>
    <td>Metadata contact</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:maintainer":{Person or Organization}</td>
    <td>Should include a name and contact point (institutional e-mail is best) for the agent responsible for metadata content. This is the contact point to report problems with metadata content.</td>
  </tr>
  <tr>
    <td>Metadata catalog</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:includedInDataCatalog": <br>{"@type": "schema:DataCatalog", "schema:name": ..., "schema:url": ...}</td>
    <td>Identifies the data catalog or repository containing this metadata record.</td>
  </tr>
  <tr>
    <td rowspan="2">Resource type</td>
    <td>1</td>
    <td>"@type":["schema:Dataset", ...]</td>
    <td>An array of schema.org type values using the schema: prefix. Must include "schema:Dataset". Additional allowed types: schema:CreativeWork, schema:SoftwareApplication, schema:SoftwareSourceCode, schema:Product, schema:WebAPI, schema:DigitalDocument, schema:Collection, schema:ImageObject, schema:DataCatalog, schema:DefinedTermSet, schema:MediaObject.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"schema:additionalType": [{DefinedTerm or string}, ...]</td>
    <td>If a more specific resource type needs to be specified from a vocabulary other than schema.org, add a text or URI value here. Must be consistent with the \@type. Always encode as an array.</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>0..1</td>
    <td>"schema:description": {string}</td>
    <td>Free text, with as much detail as is feasible</td>
  </tr>
  <tr>
    <td>Originators</td>
    <td>0..*</td>
    <td>"schema:creator": {"@list": [{Person or Organization}, ...]}</td>
    <td>Author or originator of intellectual content. Uses the JSON-LD \@list construct to preserve author order. Each item can be a Person, Organization, or an object reference ({"@id": "..."}) to an agent defined elsewhere.</td>
  </tr>
  <tr>
    <td>Publication Date</td>
    <td>0..1</td>
    <td>"schema:datePublished" : {date time}</td>
    <td>Date on which the resource was made publicly accessible. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Modification Date</td>
    <td>1</td>
    <td>"schema:dateModified" : {date time}</td>
    <td>Date of most recent update to resource content. If Publication date is not provided, defaults to the Modification Date. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Other identifiers</td>
    <td>0..*</td>
    <td>"schema:sameAs": [{URI or PropertyValue}, ...]</td>
    <td>Other identifiers for the same resource, as IRI reference strings, object references ({"@id": "..."}), or structured identifiers using schema:PropertyValue.</td>
  </tr>
  <tr>
    <td>Version</td>
    <td>0..1</td>
    <td>"schema:version": {string or number}</td>
    <td>The version number or identifier for this resource. Values should sort from oldest to newest using an alphanumeric sort.</td>
  </tr>
  <tr>
    <td>Language</td>
    <td>0..1</td>
    <td>"schema:inLanguage": {string}</td>
    <td>The language of the dataset content (e.g. "en", "fr").</td>
  </tr>
  <tr>
    <td>Measurement technique</td>
    <td>0..*</td>
    <td>"schema:measurementTechnique": {string or DefinedTerm or array}</td>
    <td>The technique, technology, or methodology used for measurement or determination of the dataset values.</td>
  </tr>
  <tr>
    <td>Keyword</td>
    <td>0..*</td>
    <td>"schema:keywords":<br>[ {string}, <br> {"@type":"schema:DefinedTerm", <br> "schema:name": "OCEANS", <br> "schema:inDefinedTermSet": "gcmd:sciencekeywords", <br> "schema:identifier": {...} },...]</td>
    <td>Implement with text for tags, and schema:DefinedTerm for keywords from a controlled vocabulary. Recommend using DefinedTerm for all keywords if any are from a known vocabulary.</td>
  </tr>
  <tr>
    <td>GeographicExtent (named place)</td>
    <td>0..*</td>
    <td>"schema:spatialCoverage": [{ "@type": "schema:Place",<br>"schema:name": {string} or {schema:DefinedTerm} }]</td>
    <td>To specify location with place names; if the names are from a gazeteer, use the schema:DefinedTerm to provide a name, identifier, and inDefinedTermSet to fully document the concept.</td>
  </tr>
  <tr>
    <td>GeographicExtent (bounding box)</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{ <br>"@type": "schema:Place",<br> "schema:geo": {  "@type": "schema:GeoShape", <br> "schema:box": "39.3280 120.1633 40.445  123.7878"   } }]</td>
    <td>For bounding box specification of the spatial extent of resource content. See <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes">ESIP SOSO for details</a>. Recommend including only one bounding box.</td>
  </tr>
  <tr>
    <td>GeographicExtent (curvilinear trace)</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{ <br>"@type": "schema:Place",<br> "schema:geo": {  "@type": "schema:GeoShape", <br> "schema:line": "39.33 120.77 40.44 123.96 41.00 121.34"   } }]</td>
    <td>For resource related to a linear trace like a ship track or airplane flight line</td>
  </tr>
  <tr>
    <td>GeographicExtent (point location)</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{<br> "@type": "schema:Place", <br>"schema:geo": {  "@type":  "schema:GeoCoordinates",  <br> "schema:latitude": 39.3280,   <br>  "schema:longitude": 120.1633 } }]</td>
    <td>For a point location specification of the spatial extent of resource content.</td>
    </tr>
  <tr>
    <td>GeographicExtent (other serialization)</th>
    <td>0..*</th>
    <td>"geosparql:hasGeometry": { <br> "@type": "sf:Point", <br> "geosparql:asWKT": {"@type":"geosparql:wktLiteral", <br>"@value":"POINT(-76  -18)"},<br> "geosparql:crs": {"@id":"http://www.opengis.net/def/crs/OGC/1.3/CRS84"} }</th>
    <td>Optional geographic extent using other more interoperable geometries, GeoSPARQL is recommended, see <a href="https://book.oceaninfohub.org/thematics/spatial/README.html#simple-geosparql-wkt">Ocean InfoHub</a>.</th>
  </tr>
  <tr>
    <td rowspan="2">Distribution Agent</td>
    <td>0..*</td>
    <td>"schema:provider":[{Person or Organization}, ...]</td>
    <td>Contact point for the provider of a distribution. For a simple digital object with a download URL, or a resource with multiple distributions all from the same provider.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"schema:distribution": [ { "@type": ["schema:DataDownload"],"schema:provider":[{Person or Organization}] }...]</td>
    <td>If there are multiple distributions with different providers, each distribution can have a separate provider array.</td>
  </tr>
  <tr>
    <td>Variable (PropertyValue)</td>
    <td>0..*</td>
    <td>"schema:variableMeasured":<br> [ { "@type":["schema:PropertyValue"],<br>&emsp; "@id": "astm:var0011",<br>&emsp;  "schema:propertyID": [ "pato:PATO_0000025",<br>&emsp;&emsp;&emsp;"astm:prop/0405" ],<br>&emsp;  "schema:name": "hostMineral", <br>&emsp; "schema:description": "...." }...]</td>
    <td>Follow <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables">ESIPfed Science on Schema.org recommendation</a>. Variable must have a name and description, should have a propertyID with URI for the represented concept.</td>
  </tr>
  <tr>
    <td>Variable (StatisticalVariable)</td>
    <td>0..*</td>
    <td>"schema:variableMeasured":<br> [ { "@type":["schema:StatisticalVariable"],<br> "@id": "astm:var0011",<br>
&emsp;"schema:measuredProperty":<br>
&emsp;&emsp;{"@type":"schema:Property", &emsp;&emsp;"schema:identifier":"astm:id/305978",<br>
&emsp;&emsp;"schema:name":"Average age"}]</td>
    <td>Statistical variable offers properties useful for describing social science statistical variables like populationType and statType. Use of StatisticalVariable is preferred for variables with values calculated from some aggregation process.</td>
  </tr>
  <tr>
    <td rowspan="5">Temporal coverage</td>
    <td rowspan="5">0..*
    </td>
    <td colspan="2">Temporal coverage is encoded as an array. Can be expressed in several ways: a calendar/clock dateTime or date time interval using ISO8601 serialization, a named time ordinal era, an interval bounded by time ordinal era, or with a numeric coordinate in a temporal reference system.</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": ["2018-01-22"]</td>
    <td>Calendar data or clock time instant use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": ["2012-09-20/2016-01-22"]</td>
    <td>Calendar data or clock time interval use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": <br> [{ "@type":"time:ProperInterval", <br> "time:intervalStartedBy": "isc:LowerDevonian", <br>  "time:intervalFinishedBy": "isc:LowerPermian" }]</td>
    <td>Time ordinal era interval, use owl:time namespace, time: http://www.w3.org/2006/time#. This example uses <a href="http://resource.geosciml.org/classifier/ics/ischart/">International chronostratigraphic chart, isc</a>. See <a href="https://perio.do/en/">PeriodO</a> for identifiers for many other named time intervals.</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": <br> [{ "time:ProperInterval- 345/298 Ma" }]</td>
    <td>For time interval specified using geologic ages, in Ka, Ma or Ga; The text string is an abbreviated owl time interval (proposal, under discussion)</td>
  </tr>
  <tr>
    <td>Related agents (contributor role)</td>
    <td>0..*</td>
    <td>"schema:contributor": [ {Person or Organization}, ... ]</td>
    <td>Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators.</td>
  </tr>
  <tr>
    <td>Related agent (other role)</td>
    <td></td>
    <td>"schema:contributor": [{"@type": "schema:Role", <br>&emsp; "schema:roleName": "Principal Investigator",<br>&emsp;"schema:contributor": {"@type": "schema:Person",&emsp;&emsp;"@id": "https://orcid.org/...",<br>&emsp;&emsp;"schema:name": "John Doe",<br>&emsp;&emsp;"schema:affiliation": {"@type": "schema:Organization",<br>&emsp;&emsp;&emsp;"@id": "https://ror.org/...",<br>&emsp;&emsp;&emsp;"schema:name": "..."},<br>&emsp;&emsp;"schema:contactPoint": {"@type": "schema:ContactPoint",<br>&emsp;&emsp;&emsp;"schema:email": "john.chodacki@ucop.edu"}}}]</td>
    <td>To assign roles to contributors like editor, maintainer, publisher, point of contact, copyright holder  (e.g.  DataCite contributor types), use the <a href="http://blog.schema.org/2014/06/introducing-role.html">role construction defined by schema.org</a></td>
  </tr>
  <tr>
    <td>Related resources</td>
    <td>0..*</td>
    <td>"schema:relatedLink": [{"@type":"schema:LinkRole", "schema:linkRelationship": "...",<br>"schema:target": {"@type": "schema:EntryPoint", <br> "schema:encodingFormat": "text/html",<br>"schema:name": "...",<br>"schema:url": "https://example.org/data/stations" } } ]</td>
    <td>Use schema.org relatedLink with a LinkRole value, and the link URL in a 'target' EntryPoint object. Use a soft-type implementation, with a link relationship type using a schema:DefinedTerm.</td>
    </tr>
  <tr>
    <td>Funding</th>
    <td>0..*</th>
    <td>"schema:funding" :<br> [{ "@type": "schema:MonetaryGrant",<br> "schema:identifier": {"@type": "schema:PropertyValue", <br>&emsp;"schema:propertyID": "grant-id", "schema:value": "..."}, <br> "schema:name": "grant title", <br> "schema:funder":<br> { "@id": "https://ror.org/...", <br> "@type": "schema:Organization", <br>  "schema:name": "org name" } }]</th>
    <td>Use schema.org encoding and <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#funding">science on schema.org pattern</a>. Other organization properties can be included in the funder/Organization.</th>
  </tr>
  <tr>
    <td>Policies</td>
    <td>0..*</td>
    <td>"schema:publishingPrinciples": [ {"@type": "schema:CreativeWork", "schema:name": "...", "schema:url": "..."}... ]</td>
    <td>FDOF digitalObjectMutability, RDA digitalObjectPolicy, FDOF PersistencyPolicy. Policies related to maintenance, update, expected time to live.</td> </tr>
<tr> <td> Checksum  </td><td> 0..1  </td><td> "schema:distribution": [ { "@type": ["schema:DataDownload"], "spdx:checksum": {<br>&nbsp;&nbsp;"@type": "spdx:Checksum",<br>&nbsp;&nbsp;"spdx:algorithm":"SHA256",<br>&nbsp;&nbsp; "spdx:checksumValue":"abc123..." },..  }...]  </td>
<td>A string value calculated from the content of the resource representation, used to test if content has been modified. No schema.org property, follow DCAT v3 adoption of <a href="https://spdx.org/rdf/terms/">Software Package Data Exchange (SPDX)</a> property; The spdx:Checksum object has two properties: algorithm and checksumValue. The checksum is a property of each distribution/DataDownload. </td></tr>
<tr >
<td colspan="4"><b>Provenance for discovery</b> is limited to documenting technology used in the creation of the dataset and documenting other datasets that were inputs to the content of the described resource. The cdifDiscovery profile specifies only that wasGeneratedBy has a prov:Activity with prov:used items that are strings or @id references. Any additional structure under prov:used is optional and defined by extended profiles.</td></tr>
<tr><td>Provenance (instruments, software etc.) </td><td>0..* </td><td>   "prov:wasGeneratedBy": [{
        "@type": ["prov:Activity"],
        "prov:used": [
            "nerc:collection/L05/current/134",
            {"@id": "nerc:collection/B76/current/B7600031"} ]
 }]</td><td>Identify sensors, instruments, platforms, software, algorithms etc. used in the creation of the described resource. The prov:used array accepts strings (URIs or labels) or object references with @id.</td></tr>
<tr>
    <td>Provenance (input datasets) </td><td>0..* </td><td>
    "prov:wasDerivedFrom": [<br>
        "http://doi.org/10.547/347848",<br>
        {"@id": "http://doi.org/10.3578/h5ls"},<br>
        {"@type": "schema:CreativeWork", "schema:name": "...", "schema:url": "..."} ]</td><td>Identify datasets that were inputs to the content of the described resource. Items can be strings (URIs), object references, or CreativeWork objects.</td></tr>
<tr>
<td colspan="4"><b>Quality information for discovery</b>: A text statement documenting quality of the resource should be included in the schema:description. If there are quality policies or certificates that apply, these should be specified in the schema:publishingPrinciples. Quality measurement or assessment protocols that have an output result specific to this resource can be specified using dqv:hasQualityMeasurement </td>
</tr><tr>
<td>Quality measure</td><td>0..*</td><td>"dqv:hasQualityMeasurement": [<br> {
"@type": "dqv:QualityMeasurement",<br>
&emsp;"dqv:isMeasurementOf": &emsp;&emsp;&nbsp;&nbsp;"nerc:collection/L27/current/ARGO_QC",
&emsp;&emsp;"dqv:value": "good" },<br>
        { "@type": "dqv:QualityMeasurement",
&emsp;&emsp;"dqv:isMeasurementOf":<br>&emsp;&emsp; "imf:dsbb/2003/eng/dqaf.htm",
&emsp;&emsp;"dqv:value":<br>
&emsp;&emsp;"http://linkToASpecificQualityReport" }]
</td><td>Quality assessment or measurement conducted using procedure or protocol specified by the dqv:isMeasurementOf property, with result value specified in the dqv:value property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment.</td>
</tr>
        </table>


---
### Source Document: metadata/archive/schemaOrgImplementationv2Reformat.md

<table class="table" border="1" style="width: 100%; table-layout: fixed; border-collapse: collapse;">
  <tr>
    <th style="width: 10%;"><b>CDIF content item</b></th>
    <th style="width: 5%;"><b>Obl.</b></th>
    <th style="width: 25%;"><b>Schema.org implementation</b></th>
    <th style="width: 60%;"><b>Scope note</b></th>
  </tr>
  <tr >
    <td >Metadata identifier</td>
    <td >1</td>
    <td > "schema:subjectOf"/"@id":{URI}</td>
    <td >The URI for the metadata record should be the \@id value for the 'schema:subjectOf' node. This node has \@type ["schema:Dataset"] with schema:additionalType ["dcat:CatalogRecord"], and a schema:about property referencing the \@id of the root resource node.</td>
  </tr>
  <tr>
    <td>Resource identifier</td>
    <td>1</td>
    <td>"schema:identifier":{PropertyValue or string}</td>
    <td>The primary identifier for the resource. Can be a simple string (ideally a resolvable URI), or a schema:PropertyValue with propertyID (identifier scheme, e.g. from <a href="https://registry.identifiers.org/registry/">identifiers.org</a>), value (the identifier string), and url (resolvable link). The PropertyValue approach is strongly recommended following the <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#identifier">ESIP Science on Schema.org guidance</a>.</td>
  </tr>
  <tr>
    <td>Title</td>
    <td>1</td>
    <td>"schema:name":{string}</td>
    <td>A set of words that should identify the described resource for human use. Ideally, should be unique in the scope of the metadata catalog containing this metadata record.</td>
  </tr>
<tr>
    <td rowspan="3">Distribution</td>
    <td rowspan="3">1</td>
    <td colspan="2">either a url or a contentURL in a distribution is required to indicate how to get the resource.</td>
</tr>
<tr>
    <td>"schema:url":{URL}</td>
    <td>This url is generally expected to GET an html landing page about the resource...</td>
</tr>
  <tr>
    <td>"schema:distribution": <br>[ {"@type": ["schema:DataDownload"], <br> "schema:contentUrl": {URL}, ... },<br> {"@type": ["schema:WebAPI"], <br> "schema:serviceType": ..., ... } ]</td>
    <td>An array of distribution objects. Items may be DataDownload (file-based access) or WebAPI (service-based access). A DataDownload must include schema:contentUrl, and should include schema:encodingFormat and dcterms:conformsTo. The \@type is encoded as an array (e.g. ["schema:DataDownload"]).</td>
  </tr>
  <tr>
    <td>Rights</td>
    <td>1..*</td>
    <td>"schema:license":[{text or URI or CreativeWork}, ...] <br> Or <br> "schema:conditionsOfAccess":[{text or URI}, ...]</td>
    <td>At least one of schema:license or schema:conditionsOfAccess must be provided (as arrays). URL to license document or text explanation of restrictions on use. There might be multiple links to documents specifying related security, privacy, usage, sharing, etc. concerns.</td>
  </tr>
  <tr>
    <td>Metadata profile identifier</td>
    <td>1..*</td>
    <td>"schema:subjectOf"/"dcterms:conformsTo": <br>[{"@id": "https://w3id.org/cdif/core/1.1/"}, <br>{"@id": "https://w3id.org/cdif/discovery/1.1/"}]</td>
    <td>An array of objects, each with an @id property whose value is a conformance URI. For CDIFDiscovery, both the core and discovery URIs are required. Extended profiles add their own conformance URIs to this array.</td>
  </tr>
  <tr>
    <td>Metadata date</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:sdDatePublished":{Date}</td>
    <td>Use ISO8601 format. The most recent publication date for the metadata content. Harvesters use this to determine if they have already harvested and processed this record.</td>
  </tr>
  <tr>
    <td>Metadata contact</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:maintainer":{Person or Organization}</td>
    <td>Should include a name and contact point (institutional e-mail is best) for the agent responsible for metadata content. This is the contact point to report problems with metadata content. Person and Organization are Agent objects with various properties.</td>
  </tr>
  <tr>
    <td>Metadata catalog</td>
    <td>0..1</td>
    <td>"schema:subjectOf"/"schema:includedInDataCatalog": <br>{"@type": "schema:DataCatalog", <br>"schema:name": ..., "schema:url": ...}</td>
    <td>Identifies the data catalog or repository containing this metadata record. Value is a schema:DataCatalog with at least a name and URL.</td>
  </tr>
  <tr>
    <td rowspan="2">Resource type</td>
    <td>1</td>
    <td>"@type":["schema:Dataset", ...]</td>
    <td>An array of schema.org type values using the schema: prefix. Must include "schema:Dataset". Additional allowed types: schema:CreativeWork, schema:SoftwareApplication, schema:SoftwareSourceCode, schema:Product, schema:WebAPI, schema:DigitalDocument, schema:Collection, schema:ImageObject, schema:DataCatalog, schema:DefinedTermSet, schema:MediaObject.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"schema:additionalType": [{DefinedTerm or string}, ...]</td>
    <td>If a more specific resource type needs to be specified using a vocabulary other than schema.org, add a text or URI value here. Must be consistent with the \@type. Always encode as an array.</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>0..1</td>
    <td>"schema:description": {string}</td>
    <td>Free text, with as much detail as is feasible</td>
  </tr>
  <tr>
    <td>Originators</td>
    <td>0..*</td>
    <td>"schema:creator": {"@list": [{Person or Organization}, ...]}</td>
    <td>Author or originator of intellectual content. Uses the JSON-LD \@list construct to preserve author order. Each item can be a Person, Organization, or an object reference ({"@id": "..."}) to an agent defined elsewhere. Use ORCID or other PID to identify persons where possible.</td>
  </tr>
  <tr>
    <td>Publication Date</td>
    <td>0..1</td>
    <td>"schema:datePublished" : {date time}</td>
    <td>Date on which the resource was made publicly accessible. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Modification Date</td>
    <td>1</td>
    <td>"schema:dateModified" : {date time}</td>
    <td>Date of most recent update to resource content. If Publication date is not provided, defaults to the Modification Date. Use ISO 8601 format.</td>
  </tr>
    <tr>
    <td>Other identifiers</td>
    <td>0..*</td>
    <td>"schema:sameAs": [{URI or PropertyValue}, ...]</td>
    <td>Other identifiers for the same resource, as IRI reference strings, object references ({"@id": "..."}), or structured identifiers using schema:PropertyValue.</td>
  </tr>
  <tr>
    <td>Version</td>
    <td>0..1</td>
    <td>"schema:version": {string or number}</td>
    <td>The version number or identifier for this resource. Values should sort from oldest to newest using an alphanumeric sort on version strings.</td>
  </tr>
  <tr>
    <td>Language</td>
    <td>0..1</td>
    <td>"schema:inLanguage": {string}</td>
    <td>The language of the dataset content (e.g. "en", "fr").</td>
  </tr>
  <tr>
    <td>Measurement technique</td>
    <td>0..*</td>
    <td>"schema:measurementTechnique": {string or DefinedTerm or array}</td>
    <td>The technique, technology, or methodology used for measurement or determination of the dataset values. Can be a string, a DefinedTerm with vocabulary reference, or an array combining these.</td>
  </tr>
  <tr>
    <td>Keyword</td>
    <td>0..*</td>
    <td>"schema:keywords":<br>[ {string}, <br> {"@type":"schema:DefinedTerm", <br> "schema:name": "OCEANS", <br> "schema:inDefinedTermSet": "gcmd:sciencekeywords", <br> "schema:identifier": {...} },...]</td>
    <td>Implement with text for tags, and schema:DefinedTerm for keywords from a controlled vocabulary. The DefinedTerm approach is used to represent concepts with links to their defining vocabulary. Recommend using DefinedTerm for all keywords if any are from a known vocabulary.</td>
  </tr>

  <tr><td colspan="4"><b>GeographicExtent</b>  Required if resource has a geographic extent for its subject, a bounding rectangle, line, or point.  To support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 84 datum. There are various other systems for describing location; these can be provided as alternate location descriptions, recognizing that they might not be meaningful to some metadata harvesting agents. Spatial coverage is encoded as an array.</td>
  </tr>
  <tr>
    <td> Named place</td>
    <td>0..*</td>
    <td>"schema:spatialCoverage": [{ "@type": "schema:Place",<br>"schema:name": {string} or {schema:DefinedTerm} }]</td>
    <td>To specify location with place names; if the names are from a gazeteer, use the schema:DefinedTerm to provide a name, identifier, and inDefinedTermSet to fully document the concept.</td>
  </tr>
  <tr>
    <td>Bounding box</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{ <br>"@type": "schema:Place",<br> "schema:geo": {  "@type": "schema:GeoShape", <br> "schema:box": "39.3280 120.1633 40.445  123.7878"   } }]</td>
    <td>For bounding box specification of the spatial extent of resource content. See <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes">ESIP SOSO for details</a>. Recommend including only one bounding box; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
  </tr>
  <tr>
    <td>Curvilinear trace</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{ <br>"@type": "schema:Place",<br> "schema:geo": {  "@type": "schema:GeoShape", <br> "schema:line": "39.33 120.77 40.44 123.96 41.00 121.34"   } }]</td>
    <td>For resource related to a linear trace like a ship track or airplane flight line</td>
  </tr>
  <tr>
    <td>Point location</td>
    <td>0..1</td>
    <td>"schema:spatialCoverage": [{<br> "@type": "schema:Place", <br>"schema:geo": {  "@type":  "schema:GeoCoordinates",  <br> "schema:latitude": 39.3280,   <br>  "schema:longitude": 120.1633 } }]</td>
    <td>For a point location specification of the spatial extent of resource content. Recommend including only one point; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
    </tr>
  <tr>
    <td>Other serialization</th>
    <td>0..*</th>
    <td>"geosparql:hasGeometry": { <br> "@type": "sf:Point", <br> "geosparql:asWKT": {"@type":"geosparql:wktLiteral", <br>"@value":"POINT(-76  -18)"},<br> "geosparql:crs": {"@id":"http://www.opengis.net/def/crs/OGC/1.3/CRS84"} }</th>
    <td>Optional geographic extent using other more interoperable geometries, GeoSPARQL is recommended, see <a href="https://book.oceaninfohub.org/thematics/spatial/README.html#simple-geosparql-wkt">Ocean InfoHub</a>. Other geometry schemes might be specified in a specific domain profile, e.g. for atmospheric, subsurface data, or local coordinate systems.</th>
  </tr>
  <tr><td colspan="4"><b>Distribution</b></td></tr>
  <tr>
    <td rowspan="2">Distribution Agent</td>
    <td>0..*</td>
    <td>"schema:provider":[{Person or Organization}, ...]</td>
    <td>Contact point for the provider of a distribution. For a simple digital object with a download URL, or a resource with multiple distributions all from the same provider.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"schema:distribution": [ { "@type": ["schema:DataDownload"],"schema:provider":[{Person or Organization}] }...]</td>
    <td>If there are multiple distributions with different providers, each distribution can have a separate provider array.</td>
  </tr>
  <tr><td colspan="4"><b>Variables in the data</b>  The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be, ideally, qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text. </td></tr>
  <tr>
    <td>Variable (PropertyValue)</td>
    <td>0..*</td>
    <td>"schema:variableMeasured":<br> [ { "@type":["schema:PropertyValue"],<br>&emsp; "@id": "astm:var0011",<br>&emsp;  "schema:propertyID": [ "pato:PATO_0000025",<br>&emsp;&emsp;&emsp;"astm:prop/0405" ],<br>&emsp;  "schema:name": "hostMineral", <br>&emsp; "schema:description": "...." }...]</td>
    <td>Follow <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables">ESIPfed Science on Schema.org recommendation</a>, see also discussion for representing more complex data structures in <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Experimental.md#AdvancedVariableValueType">ESIPfed Experimental</a> and the <a href="https://cross-domain-interoperability-framework.github.io/cdifbook/data_integration/ddidescriptiondatastructure.html">Data Integration module of CDIF</a>. Variable must have a name and description, should have a propertyID with URI for the represented concept. The URI in the propertyID provides the semantic linkage for meaning of the variable.</td>
  </tr>
  <tr>
    <td>Variable (StatisticalVariable)</td>
    <td>0..*</td>
    <td>"schema:variableMeasured":<br> [ { "@type":["schema:StatisticalVariable"],<br> "@id": "astm:var0011",<br>
&emsp;"schema:measuredProperty":<br>
&emsp;&emsp;{"@type":"schema:Property", &emsp;&emsp;"schema:identifier":"astm:id/305978",<br>
&emsp;&emsp;"schema:name":"Average age"}]</td>
    <td>Statistical variable offers properties useful for describing social science statistical variables like populationType and statType. Use of StatisticalVariable is preferred for variables with values calculated from some aggregation process.</td>
  </tr>
  <tr>
    <td rowspan="5">Temporal coverage</td>
    <td rowspan="5">0..*
    </td>
    <td colspan="2">Temporal coverage is encoded as an array. Can be expressed in several ways: a calendar/clock dateTime or date time interval using ISO8601 serialization, a named time ordinal era, an interval bounded by time ordinal era, or with a numeric coordinate in a temporal reference system.</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": ["2018-01-22"]</td>
    <td>Calendar data or clock time instant use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": ["2012-09-20/2016-01-22"]</td>
    <td>Calendar data or clock time interval use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": <br> [{ "@type":"time:ProperInterval", <br> "time:intervalStartedBy": "isc:LowerDevonian", <br>  "time:intervalFinishedBy": "isc:LowerPermian" }]</td>
    <td>Time ordinal era interval, use owl:time namespace, time: http://www.w3.org/2006/time#. This example uses <a href="http://resource.geosciml.org/classifier/ics/ischart/">International chronostratigraphic chart, isc</a>. See <a href="https://perio.do/en/">PeriodO</a> for identifiers for many other named time intervals.</td>
  </tr>
  <tr>
    <td>"schema:temporalCoverage": <br> [{ "time:ProperInterval- 345/298 Ma" }]</td>
    <td>For time interval specified using geologic ages, in Ka, Ma or Ga; The text string is an abbreviated owl time interval (proposal, under discussion)</td>
  </tr>
  <tr>
    <td>Related agents (contributor role)</td>
    <td>0..*</td>
    <td>"schema:contributor": [ {Person or Organization}, ... ]</td>
    <td>Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators.</td>
  </tr>
  <tr>
    <td>Related agent (other role)</td>
    <td></td>
    <td>"schema:contributor": [{"@type": "schema:Role", <br>&emsp; "schema:roleName": "Principal Investigator",<br>&emsp;"schema:contributor": {"@type": "schema:Person",&emsp;&emsp;"@id": "https://orcid.org/...",<br>&emsp;&emsp;"schema:name": "John Doe",<br>&emsp;&emsp;"schema:affiliation": {"@type": "schema:Organization",<br>&emsp;&emsp;&emsp;"@id": "https://ror.org/...",<br>&emsp;&emsp;&emsp;"schema:name": "..."},<br>&emsp;&emsp;"schema:contactPoint": {"@type": "schema:ContactPoint",<br>&emsp;&emsp;&emsp;"schema:email": "john.chodacki@ucop.edu"}}}]</td>
    <td>To assign roles to contributors like editor, maintainer, publisher, point of contact, copyright holder  (e.g.  DataCite contributor types), use the <a href="http://blog.schema.org/2014/06/introducing-role.html">role construction defined by schema.org</a></td>
  </tr>
  <tr>
    <td>Related resources</td>
    <td>0..*</td>
    <td>"schema:relatedLink": [{"@type":"schema:LinkRole", "schema:linkRelationship": "...",<br>"schema:target": {"@type": "schema:EntryPoint", <br> "schema:encodingFormat": "text/html",<br>"schema:name": "...",<br>"schema:url": "https://example.org/data/stations" } } ]</td>
    <td>Use schema.org relatedLink with a LinkRole value, and the link URL in a 'target' EntryPoint object. These properties expect WebPage and Action as their domain, so the <a href="https://validator.schema.org/">schema.org validator</a> will throw a warning (not an error). Related resource links are useful for evaluation and use of data, but because of the wide variety of relationship possibilities, difficult to use in general search scenarios. Use a soft-type implementation, with a link relationship type using a schema:DefinedTerm, and a resolvable identifier for the relationship target.</td>
    </tr>
  <tr>
    <td>Funding</th>
    <td>0..*</th>
    <td>"schema:funding" :<br> [{ "@type": "schema:MonetaryGrant",<br> "schema:identifier": {"@type": "schema:PropertyValue", <br>&emsp;"schema:propertyID": "grant-id", "schema:value": "..."}, <br> "schema:name": "grant title", <br> "schema:funder":<br> { "@id": "https://ror.org/...", <br> "@type": "schema:Organization", <br>  "schema:name": "org name" } }]</th>
    <td>Use schema.org encoding and <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#funding">science on schema.org pattern</a>. Other organization properties can be included in the funder/Organization.</th>
  </tr>
  <tr>
    <td>Policies</td>
    <td>0..*</td>
    <td>"schema:publishingPrinciples": [ {"@type": "schema:CreativeWork", "schema:name": "...", "schema:url": "..."}... ]</td>
    <td>FDOF digitalObjectMutability, RDA digitalObjectPolicy, FDOF PersistencyPolicy. Policies related to maintenance, update, expected time to live.</td> </tr>
<tr> <td> Checksum  </td><td> 0..1  </td><td> "schema:distribution": [ { "@type": ["schema:DataDownload"], "spdx:checksum": {<br>&nbsp;&nbsp;"@type": "spdx:Checksum",<br>&nbsp;&nbsp;"spdx:algorithm":"SHA256",<br>&nbsp;&nbsp; "spdx:checksumValue":"abc123..." },..  }...]  </td>
<td>A string value calculated from the content of the resource representation, used to test if content has been modified. No schema.org property, follow DCAT v3 adoption of <a href="https://spdx.org/rdf/terms/">Software Package Data Exchange (SPDX)</a> property; The spdx:Checksum object has two properties: algorithm and checksumValue. The checksum is a property of each distribution/DataDownload. </td></tr>
<tr >
<td colspan="4"><b>Provenance for discovery</b> is limited to documenting technology used in the creation of the dataset and documenting other datasets that were inputs to the content of the described resource. The cdifDiscovery profile specifies only that wasGeneratedBy has a prov:Activity with prov:used items that are strings or @id references. Any additional structure under prov:used is optional and defined by extended profiles.</td></tr>
<tr><td>Provenance (instruments, software etc.) </td><td>0..* </td><td>   "prov:wasGeneratedBy": [{
        "@type": ["prov:Activity"],
        "prov:used": [
            "nerc:collection/L05/current/134",
            {"@id": "nerc:collection/B76/current/B7600031"} ]
 }]</td><td>Identify sensors, instruments, platforms, software, algorithms etc. used in the creation of the described resource. The prov:used array accepts strings (URIs or labels) or object references with @id.</td></tr>
<tr>
    <td>Provenance (input datasets) </td><td>0..* </td><td>
    "prov:wasDerivedFrom": [<br>
        "http://doi.org/10.547/347848",<br>
        {"@id": "http://doi.org/10.3578/h5ls"},<br>
        {"@type": "schema:CreativeWork", "schema:name": "...", "schema:url": "..."} ]</td><td>Identify datasets that were inputs to the content of the described resource. Items can be strings (URIs), object references, or CreativeWork objects with name and URL.</td></tr>
<tr>
<td colspan="4"><b>Quality information for discovery</b>: A text statement documenting quality of the resource should be included in the   schema:description. If there are quality policies or certificates that apply, these should be specified in the schema:publishingPrinciples. Quality measurement or assessment protocols that have an output result specific to this resource can be specified using dqv:hasQualityMeasurement </td>
</tr><tr>
<td>Quality measure</td><td>0..*</td><td>"dqv:hasQualityMeasurement": [<br> {
"@type": "dqv:QualityMeasurement",<br>
&emsp;"dqv:isMeasurementOf": &emsp;&emsp;&nbsp;&nbsp;"nerc:collection/L27/current/ARGO_QC",
&emsp;&emsp;"dqv:value": "good" },<br>
        { "@type": "dqv:QualityMeasurement",
&emsp;&emsp;"dqv:isMeasurementOf":<br>&emsp;&emsp; "imf:dsbb/2003/eng/dqaf.htm",
&emsp;&emsp;"dqv:value":<br>
&emsp;&emsp;"http://linkToASpecificQualityReport" }]
</td><td>Quality assessment or measurement conducted using procedure or protocol specified by the dqv:isMeasurementOf property, with result value specified in the dqv:value property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment.</td>
</tr>
        </table>



---
### Source Document: metadata/archive/schemaorgimplementation.md

# Schema.org implementation of CDIF metadata 

JSON-LD has been chosen as the recommended serialization format for CDIF metadata following our principle to use existing mainstream technology. The JSON format is widely used for data serialization and popular with developers. JSON-LD adds additional syntax for the representation of linked data, compatible with existing JSON implementations so that integration with existing applications is relatively frictionless. Many metadata providers are using the [schema.org](https://schema.org/) vocabulary with JSON-LD serialization for metadata publication and interchange. Use of this format provides a low barrier to entry for data providers.

The JSON syntax is defined by the [ECMA JSON specification](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/), and JSON-LD is specified in the [JSON-LD 1.1 recommendation](https://www.w3.org/TR/json-ld11/) from the World Wide Web Consortium (W3C). This serialization is designed for linked data applications that will translate the JSON into a set of {subject, predicate, object} triples that can be loaded into an RDF database for processing. The JSON-LD context binds JSON keys to URIs for more precise semantics, and the use of URIs to identify entities and property values in the metadata will maximize the linkage with resources on the wider web to build an ever-expanding global knowledge graph.

The metadata about the resource has properties about the resource like title, description, responsible parties, spatial or temporal extent (as outlined in the [Metadata Content Requirements](./contentmodel.md) section).

In a harvesting/federated catalog system some metadata about the metadata is useful to keep track of where metadata came from, what format/profile it uses (harvesters need this to process), and update dates [see Metadata Content Requirements](./contentmodel.md). Unambiguous expression of this information requires making statements about a metadata record distinct from the thing in the world that the metadata describes. In an RDF framework, this requires a distinct identifier for the metadata record object that will serve as the subject for these triples.

Schema.org includes several properties that can be used to embed information about the metadata record in the resource metadata: [**sdDatePublished**](https://schema.org/sdDatePublished), [**sdLicense**](https://schema.org/sdLicense), [**sdPublisher**](https://schema.org/sdPublisher), but lacks a way to provide an identifier for the metadata record distinct from the resource it describes, to specify other agents responsible for the metadata except the publisher, or to assert specification or profile conformance for the metadata record itself.

In the RDF serialization, Schema.org metadata records are [JSON-LD node objects](https://www.w3.org/TR/json-ld/#node-objects), and include an "@id" keyword with a value that identifies the node, analogous to a primary key in a relational database.  This identifier can be interpreted to represent a thing in the world that the metadata record (the 'node') is about, or to represent the metadata record (a JSON object) itself. 

To avoid this ambiguity, CDIF adopts the convention that the schema.org identifier property is used to identify a thing in the world that is the subject of the JSON-LD node.  The identified thing might be physical, imaginary, abstract, or a digital object.  The JSON-LD @id property identifies a node in a graph, which is an abstract object. As a URI the @id URI is expected to dereference to produce a JSON-LD object containing the properties that are attached to the graph node. Given this convention, when the metadata record is processed, the processor should use the schema:identifier as subject of triples about the subject of the metadata record to avoid ambiguity.  In addition, this convention would suggest that if a schema:identifier property is present, the @id property should be interpreted to identify the JSON object that is the representation of the node in the knowledge graph. 

Statements about the metadata record (the JSON object) as a distinct entity should be made using a separate identified node object. This node object can be embedded in the metadata record about the resource in the world (Example 1 below), or published as a separate node (Example 2 below). Note that this second approach is like the [DCAT CatalogRecord](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record). 

```
{   "@context": [
        "https://schema.org",
        {"dcterms": "http://purl.org/dc/terms/",
         "ex":"https://example.com/99152/"
        }
    ],
    "@id": "ex:URIforNode1",
    "@type": "appropriate schema.org type",
	"identifier":"ex:URIforDescribedResource",
    "name": "unique title for the resource",
    "description": "Description of the resource",
    "subjectOf": {
        "@id": "ex:URIforNode2",
        "@type": "DigitalDocument",
        "dateModified": "2017-05-23",
		"identifier":"ex:URIforNode1",
        "description":"metadata about documentation for ex:URIforDescribedResource",
    	"dcterms:conformsTo": {"@id":"CDIF_basic_1.0"}
	}        
   }
```
Example 1.  Metadata about the metadata embedded.

```
{
    "@context": [
        "https://schema.org",
        {"ex": "https://example.com/99152/"}
    ],
    "@graph": [
        {
            "@id": "ex:URIforNode1",
            "@type": "Dataset",
            "identifier": "ex:URIforDescribedResource",
            "name": "unique title for the resource",
            "description": "Description of the resource"
        },
        {
            "@id": "ex:URIforNode2",
            "@type": "DigitalDocument",
            "dateModified": "2017-05-23",
            "identifier": "ex:URIforNode1",
            "description": "metadata about documentation for ex:URIforDescribedResource",
            "dcterms:conformsTo": {"@id": "CDIF_basic_1.0"}
        }
    ]
}
```

Example 2. Metadata about metadata as a separate graph node.

The ex namespace in the example above is only included so the example is valid; actual metadata would likely have its own namespace for resource and metadata URIs. The distinct identifier for the metadata record (ex:URIforNode1) allows statements to be made about the metadata separately from statements about the resource it describes. 

Note that the @type for the metadata node (root node) is 'DigitalDocument'. This is a schema.org type that corresponds broadly to the concept of DigitalObject as used by the Fair Digital Object (FDO) community ([Bonino et al., 2022](https://fairdigitalobjectframework.org/) ), recognizing that the metadata record is a digital object. 

JSON keys prefixed with '@' are keywords defined in the [JSON-LD specification]( https://www.w3.org/TR/json-ld11/#keywords) (see table below)

 | Keyword  |   Description|
 |-----------|-------------|
 | \@context |  The value of the context is an object that specifies set of rules for interpreting the JSON-LD document. The rules can be specified inline in, or via a URI that identifies a context object containing a set of rules. |
|  \@id    |    A string that identifies the subject of the assertions in the JSON object that contains the \@id key.|
|  \@type   |   An identifier for the definition of the structure of the JSON object that contains the \@type key. The type determines what keys or values should be expected in the JSON object that contains the key. Values are types defined in the schema.org vocabulary. In the CDIF framework (and for compatibility with FDOF FDOF digitalObjectType), the schema:additionalType property should be used (see implementation table below) |
 

# Implementation of metadata content items

The following table maps the metadata content items described in the [Metadata Content Requirements](./contentmodel.md) section to the schema.org JSON-LD keys to use in metadata serialization. Some example metadata documents follow. The \'Obl.\' column specifies the cardinality obligation for the property; \'1\' means one value required; 1..\* means at least one value is required; 0..\* means the property is optional and more that one value can be provided. Properties with path from "subjectOf" describe the metadata.

<table class="table">
  <tr>
    <th><b>CDIF content<br>item</b></th>
    <th><b>Obl.</b></th>
    <th><b>Schema.org<br> implementation</b></th>
    <th><b>Scope note</b></th>
  </tr>
  <tr >
    <td>Metadata identifier</td>
    <td>1</td>
    <td>"subjectOf"/"@id":{URI} or "@id":{uri} in node with "identifier":"@id" of the node containing the resource description</td>
    <td>The URI for the metadata record should be the \@id value for the 'subjectOf' element in the JSON instance document tree or "@id":{uri} in a separate graph node with "identifier":"@id" of the node containing the resource description</td>
  </tr>
  <tr>
    <td>Resource identifier</td>
    <td>1</td>
    <td>"identifier":{URI}</td>
    <td>The URI for the resource that is the subject of the metadata record should be the "identifier": value for the root of the JSON instance document tree</td>
  </tr>
  <tr>
    <td>Title</td>
    <td>1</td>
    <td>"name":{string}</td>
    <td>A set of words that should uniquely identify the described resource for human use, in the scope of the metadata catalog containing this metadata record.</td>
  </tr>
  <tr>
    <td rowspan="2">Distribution</td>
    <td>1</td>
    <td>"url":{URL}</td>
    <td>If metadata is about a single digital object</td>
  </tr>
  <tr>
    <td></td>
    <td>"distribution": <br> { "@type": "DataDownload", <br> "contentUrl": {URL },\... }</td>
    <td>If the metadata is about an abstract, non-digital, or physical resource that has multiple distributions, with different URL, encodingFormat, conformsTo properties. Each distribution is considered a distinct digital object. The dataDownload MUST include the contentUrl, and SHOULD include encodingFormat, dcterms:conformsTo to specify the media type and specification or profile documenting the specific serialization conventions for the download content.</td>
  </tr>
  <tr>
    <td>Rights</td>
    <td>1..*</td>
    <td>"license":{text or URI} <br> Or <br> "conditionsOfAccess":{text or URI}</td>
    <td>URL to license document or text explanation of restrictions on use. There might be multiple links to documents specifying related security, privacy, usage, sharing, etc... concerns.</td>
  </tr>
  <tr>
    <td>Metadata profile identifier</td>
    <td>1</td>
    <td>"subjectOf"/"dcterms:conformsTo": {identifier}</td>
    <td>Use Dublin Core terms property. The value for Base CDIF metadata is 'CDIF_basic_1.0' [tbd; this should be a PID]. Different profiles extending this must define unique identifier strings to use here. Note that the schema.org schemaVersion is used to indicate the version of the schema.org vocabulary, but in general this is not needed for CDIF.</td>
  </tr>
  <tr>
    <td>Metadata date</td>
    <td>0..1</td>
    <td>"subjectOf"/"dateModified":{Date or DateTime}</td>
    <td>Use ISO8601 format. The most recent update date for the metadata content. Harvesters use this to determine if they have already harvested and processed this record.</td>
  </tr>
  <tr>
    <td>Metadata contact</td>
    <td>0..1</td>
    <td>/ "subjectOf"/"maintainer":{Person or Organization}</td>
    <td>Should include a name and contact point (institutional e-mail is best) for the agent responsible for metadata content. This is the contact point to report problems with metadata content. Person and Organization are Agent objects with various properties.</td>
  </tr>
  <tr>
    <td rowspan="2">Resource type</td>
    <td>1</td>
    <td>"@type":{schema.org type}</td>
    <td>Use the most specific [Schema.org resource type](https://schema.org/docs/full.html) that is applicable. Multiple value can be provided but they must be logically consistent.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"additionalType": [{DefinedTerm or URI}, ...]</td>
    <td>If a more specific resource type needs to be specified, add a text or URI value here that identifies the type. MUST be consistent with the \@type. To simplify parsing, always encode as an array.</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>0..1</td>
    <td>"description": {string}</td>
    <td>Free text, with as much detail as is feasible</td>
  </tr>
  <tr>
    <td>Originators</td>
    <td>0..*</td>
    <td>"creator" : [{Person or Organization}, ...]</td>
    <td>The value is a schema.org person or organization. To simplify parsing, always encode as an array. Use ORCID or other PID to identify person or organization where possible</td>
  </tr>
  <tr>
    <td>Publication Date</td>
    <td>0..1</td>
    <td>"datePublished" : {date time}</td>
    <td>Date on which the resource was made publicly accessible. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Modification Date</td>
    <td>1</td>
    <td>"dateModified" : {date time}</td>
    <td>Date of most recent update to resource content. If Publication date is not provided, defaults to the Modification Date. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Keyword</td>
    <td>0..*</td>
    <td>"keywords":<br>[ {string}, <br> {"@type":"DefinedTerm", <br> "name": "OCEANS", <br> "inDefinedTermSet": "gcmd:sciencekeywords", <br> "identifier": "gcmd:concept/916b....6167d" },...]</td>
    <td>Implement with text for tags, and schema:DefinedTerm for keywords from a controlled vocabulary. The DefinedTerm approach is used to represent concepts.</td>
  </tr>
  
  <tr><td colspan="4"><b>GeographicExtent</b>  Required if resource has a geographic extent for its subject, a bounding rectangle, line, or point.  To support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 84 datum. There are various other systems for describing location; these can be provided as alternate location descriptions, recognizing that they might not be meaningful to some metadata harvesting agents.</td>
  </tr>
  <tr>
    <td> Named place</td>
    <td>0..*</td>
    <td>"spatialCoverage": { "@type": "Place",<br>"name": {string} or {schema:DefinedTerm} }</td>
    <td>To specify location with place names; if the names are from a gazeteer, use the schema:DefinedTerm to provide a name, identifier, and inDefinedTermSet to fully document the concept.</td>
  </tr>
  <tr>
    <td>Bounding box</td>
    <td>0..1</td>
    <td>"spatialCoverage": { <br>"@type": "Place",<br> "geo": {  "@type": "GeoShape", <br> "box": "39.3280 120.1633 40.445  123.7878"   } }</td>
    <td>For bounding box specification of the spatial extent of resource content. See [ESIP SOSO for details](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes). Recommend including only one bounding box; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
  </tr>
  <tr>
    <td>Curvilinear trace</td>
    <td>0..1</td>
    <td>"spatialCoverage": { <br>"@type": "Place",<br> "geo": {  "@type": "GeoShape", <br> "line": "39.33 120.77 40.44 123.96 41.00 121.34"   } }</td>
    <td>For resource related to a linear trace like a ship track or airplane flight line</td>
  </tr>
  <tr>
    <td>Point location</td>
    <td>0..1</td>
    <td>"spatialCoverage": {<br> "@type": "Place", <br>"geo": {  "@type":  "GeoCoordinates",  <br> "latitude": 39.3280,   <br>  "longitude": 120.1633 } }</td>
    <td>For a point location specification of the spatial extent of resource content. Recommend including only one point; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
    </tr>
  <tr>
    <td>Other serialization</th>
    <td>0..*</th>
    <td>"geosparql:hasGeometry": { <br> "@type": "sf#Point", <br> "geosparql:asWKT":  "@type":#wktLiteral", <br>"@value":"POINT(-76  -18)"},<br> "Geosparql:crs": {"@id":"CRS84"} }</th>
    <td>Optional geographic extent using other more interoperable geometries, GeoSPARQL us recommended, see <a href="https://book.oceaninfohub.org/thematics/spatial/README.html#simple-geosparql-wkt">Ocean InfoHub</a>. (Note URIs in example are truncated...) Other geometry schemes might be specified in a specific domain profile, e.g. for atmospheric, subsurface data, or local coordinate systems.</th>
  </tr>
  <tr><td colspan="4"><b>Distribution</b></td></tr>
  <tr>
    <td rowspan="2">Distribution Agent</td>
    <td>0..*</td>
    <td>"provider":{Person or Organization}</td>
    <td>Contact point for the provider of a distribution. For a simple digital object with a download URL, or a resource with multiple distributions all from the same provider.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"distribution": [ { "@type": "DataDownload","provider":{Person or Organization} }...]</td>
    <td>If there are multiple distributions with different providers, each distribution can have a separate provider</td>
  </tr>
  <tr><td colspan="4"><b>Variables in the data</b>  Required for datasets. The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be, ideally, qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text. </td></tr>
  <tr>
    <td>Variable (PropertyValue)</td>
    <td>0..*</td>
    <td>"variableMeasured":<br> [ { "@type":"PropertyValue",<br>&emsp; "@id": "astm:var0011",<br>&emsp;  "propertyID": [ "pato:PATO_0000025",<br>&emsp;&emsp;&emsp;"astm:prop/0405" ],<br>&emsp;  "name": "hostMineral", <br>&emsp; "description": "...." }...]</td>
    <td>Follow <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables">ESIPfed Science on Schema.org recommendation</a>, see also discussion for representing more complex data structures in <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Experimental.md#AdvancedVariableValueType">ESIPfed Experimental</a> and the <a href="https://cross-domain-interoperability-framework.github.io/cdifbook/data_integration/ddidescriptiondatastructure.html">Data Integration module of CDIF</a>. Variable must have a name and description, should have a propertyID with URI for the represented concept. The URI in the propertyID provides the semantic linkage for meaning of the variable.</td>
  </tr>
  <tr>
    <td>Variable (StatisticalVariable)</td>
    <td>0..*</td>
    <td>"variableMeasured":<br> [ { "@type":"StatisticalVariable",<br> "@id": "astm:var0011",<br>"@type": "StatisticalVariable",<br>
&emsp;"measuredProperty":<br>
&emsp;&emsp;{"@type":"Property",      &emsp;&emsp;"identifier":"astm:id/305978",<br>
&emsp;&emsp;"name":"Average age"}]</td>
    <td>Statistical variable offers properties useful for describing social science statistical variables like populationType and statType. Use of StatisticalVariable is preferred for variables with values calculated from some aggregation process.</td>
  </tr>
  <tr>
    <td rowspan="5">Temporal coverage</td>
    <td rowspan="5">0..*
    </td>
    <td colspan="2">Temporal coverage can be expressed in several ways: a calendar/clock dateTime or date time interval using ISO8601 serialization, a named time ordinal era, an interval bounded by time ordinal era, or with a numeric coordinate in a temporal reference system.</td>
  </tr>
  <tr>
    <td>"temporalCoverage": "2018-01-22"</td>
    <td>Calendar data or clock time instant use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"temporalCoverage": "2012-09-20/2016-01-22"</td>
    <td>Calendar data or clock time interval use ISO8601 encoding</td>
  </tr>
  <tr> 
    <td>"temporalCoverage": <br> [{ "@type":"time:ProperInterval", <br> "time:intervalStartedBy": "isc:LowerDevonian, <br>  "time:intervalFinishedBy": "isc:LowerPermian" }]</td>
    <td>Time ordinal era interval, use owl:time namespace, time: http://www.w3.org/2006/time#. This example uses <a href="http://resource.geosciml.org/classifier/ics/ischart/">International chronostratigraphic chart, isc</a>. See <a href="https://perio.do/en/">PeriodO</a> for identifiers for many other named time intervals.</td>
  </tr>
  <tr>
    <td>"temporalCoverage": <br> [{ "time:ProperInterval- 345/298 Ma" }]</td>
    <td>For time interval specified using geologic ages, in Ka, Ma or Ga; The text string is an abbreviated owl time interval (proposal, under discussion)</td>
  </tr>
  <tr>
    <td>Related agents (contributor role)</td>
    <td>0..*</td>
    <td>"contributor": [ {Person or Organization}, ... ]</td>
    <td>Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators.</td>
  </tr>
  <tr>
    <td>Related agent (other role)</td>
    <td></td>
    <td>"contributor": {"@type": "Role", <br>&emsp; "roleName": "Principal Investigator",<br>&emsp;"contributor": {"@type": "Person",&emsp;&emsp;"@id": "https://orcid.org/...",<br>&emsp;&emsp;"name": "John Doe",<br>&emsp;&emsp;"affiliation": {"@type": "Organization",<br>&emsp;&emsp;&emsp;"@id": "https://ror.org/...",<br>&emsp;&emsp;&emsp;"name": "..."},<br>&emsp;&emsp;"contactPoint": {"@type": "ContactPoint",<br>&emsp;&emsp;&emsp;"email": "john.chodacki@ucop.edu"}</td>
    <td>To assign roles to contributors like editor, maintainer, publisher, point of contact, copyright holder  (e.g.  DataCite contributor types), use the rather convoluted <a href="http://blog.schema.org/2014/06/introducing-role.html">role construction defined by schema.org</a></td>
  </tr>
  <tr>
    <td>Related resources</td>
    <td>0..*</td>
    <td>"relatedLink": [{"@type":"LinkRole", "linkRelationship": "...",<br>"target: {"@type": "EntryPoint", <br> "encodingType": "text/html",<br>"name": "...",<br>"url": "https://example.org/data/stations" } } ]</td>
    <td>Use schema.org relatedLink with a LinkRole value, and the link URL in a 'target' EntryPoint object. These properties expect WebPage and Action as their domain, so the <a href="https://validator.schema.org/">schema.org validator</a> will throw a warning (not an error). Related resource links are useful for evaluation and use of data, but because of the wide variety of relationship possibilities, difficult to use in general search scenarios. Use a soft-type implementation, with a link relationship type using a schema:DefinedTerm, and a resolvable identifier for the relationship target.</td>
    </tr>
  <tr>
    <td>Funding</th>
    <td>0..*</th>
    <td>"funding" :<br> { "@id": "URI for grant", <br> "@type": "MonetaryGrant",<br> "identifier": "grant id",  <br> "name": "grant title", <br> "funder":<br> { "@id": "ror for org", <br> "@type": "Organization", <br>  "name": "org name",  <br> "identifier": [ "other identifiers" ] } }</th>
    <td>Use schema.org encoding and <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#funding">science on schema.org pattern</a>. Other organization properties can be included in the funder/Organization.</th>
  </tr>
  <tr>
    <td>Policies</td>
    <td>0..*</td>
    <td>"publishingPrinciples": [ {"@type": "CreativeWork"}.... ]</td>
    <td>FDOF digitalObjectMutability, RDA digitalObjectPolicy, FDOF PersistencyPolicy. Policies related to maintenance, update, expected time to live.</td> </tr>
<tr> <td> Checksum  </td><td> 0..1  </td><td> "distribution\": \[ { \"@type\": \"DataDownload\",    \"spdx:checksum\": {<br>&nbsp;&nbsp;"spdx:algorithm":"string",<br>&nbsp;&nbsp; "spdx:checksumValue":"string" },..  }\...\]  </td>
<td>A string value calculated from the content of the resource representation, used to test if content has been modified. No schema.org property, follow DCAT v3 adoption of [Software Package Data Exchange (SPDX)](https://spdx.org/rdf/terms/) property; The [spdx Checksum object](https://spdx.org/rdf/spdx-terms-v2.1/classes/Checksum___-238837136.html) has two properties: algorithm and checksumValue. The checksum is a property of each distribution/DataDownload. </td></tr>
<tr >
<td colspan="4"><b>Provenance for discovery</b> is limited to documenting technology used in the creation of the dataset and documening other datasets (datasets) that were inputs to the content of the described resource.</td></tr>
<tr><td>Provenance (instruments, software etc.) </td><td>|0..* </td><td>   "prov:wasGeneratedBy": {
        "@type": "prov:Activity",
        "prov:used": [
            "nerc:collection/L05/current/134",
            "nerc:collection/B76/current/B7600031" ]
 },</td><td>Identify sensors, instruments, platforms, software, algorithms etc. used in the creation of the described resource</td></tr>
    <td>Provenance (input datasets) </td><td>|0..* </td><td>   
    "prov:wasDerivedFrom": [<br>
        "http://doi.org/10.547/347848",
        "http://doi.org/10.3578/h5ls",
        "http://doi.org/10.547/93578" ],</td><td>"</td></tr>
<tr>
<td colspan="4"><b>Quality information for discovery</b>: A text statement documenting quality of the resource should be included in the   sdo:description. If there are quality policies or certificates that apply, these should be specified in the sdo:policies. Quality measurement or assessment protocols that have an output result specific to this resource can be specified using dqv:hasQualityMeaurement </td>
</tr><tr>
<td>Quality measure</td><td>0..*</td><td>"dqv:hasQualityMeasurement": [<br> {
"@type": "dqv:QualityMeasurement",<br>
&emsp;"dqv:isMeasurementOf": &emsp;&emsp;&nbsp;&nbsp;"nerc:collection/L27/current/ARGO_QC",
&emsp;&emsp;"dqv:value": "good" },<br>
        { "@type": "dqv:QualityMeasurement",
&emsp;&emsp;"dqv:isMeasurementOf":<br>&emsp;&emsp; "imf:dsbb/2003/eng/dqaf.htm",
&emsp;&emsp;"dqv:value":<br>
&emsp;&emsp;"http://linkToASpecificQualityReport" }]
</td><td>Quality assesment or measument conducted using procedure or protocol specified by the dqv:isMeasurementOf property, with result value specified in the dqv:value property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment.</td>
</tr>
        </table>


# Service-based distribution

An API builds on a basic communication protocol (e.g. HTTP) by defining functionality and formatting to enable providing the specific data a user requires. This might involve filtering, subsetting, or various transformations for e.g. schema mapping, aggregating or anonymizing data. The focus here is on Web APIs that provide data using a URL for the endpoint location (the server that implements the data access protocol), with parameters to specify the particular data requested. The query parameters might be appended to this base URL as part of the URL, or provided as a message with the request.  The implementation is based on the schema.org Action patterns, and the WebAPI is added as as a type for the value of sdo:distribution, analogous to dcat:accessService/dcat:DataService. 

Implementation of metadata to describe a service-based (API) distribution:

| **CDIF content item**       | **Obl.** | **Schema.org implementation**   | **Scope note**                              |
|----------- |-------------|-------------|-------------|
| Service type | 1 | "distribution"/"WebAPI"/<br>"serviceType": "string"| specify the kind of service. Ideally this should be a resolvable identifier. Currently there is no widely adopted registry for serviceType identifiers, in large part because services might be defined at different levels of granularity, and classifications might focus on function, data formats, thematic content, security, or other aspects of the service definition. For interoperability, there must be an external arrangement between data providers and consumers on the strings that will be used to specify service types.  |
| Service description document | 0..1 | "distribution"/"WebAPI"/"documentation": "string" OR CreativeWork | document that provides a machine-actionable description of a service instance. Examples include OpenAPI documents, OGC Capabilities documents. Software designed to utilise a particular service type will typically include functionality to parse such a description document and engage with the service endpoint. |
| Endpoint URL | 1 | "distribution"/"WebAPI"/<br>"potentialAction"//"target"//<br>"urlTemplate" | Web location to invoke service; if there are parameters on the URL, the URL temple construct enables description of the parameters |
| Access constraints | 1 | "distribution"/"WebAPI"/"termsOfService":<br>"string" OR CreativeWork | Description of access privileges required to use the API, e.g. registration, licensing, payments. Note that access constraints applying to any distribution of the resource should be specified in the access constraints for the resource description as a whole. |


# Implementation patterns

-   DefinedTerm. {label, schemename, conceptURI, schemeURI}. This is a pattern used for property values that are concepts defined in a controlled vocabulary, ontology, or similar semantic artefact. Values have a label, which is a string that will be meaningful to a human user, a 'schemename', which is a label that similarly identifies the source semantic resource in which the concept is defined, the conceptURI is a globally unique,resolvable identifier forthe concept value; schemeURI is a globally unique identifier for the semantic resource in which the concept is defined.

-   Identifier. Identifiers can be inserted as simple string literals. If the identifier can be provided as a string literal that is resolvable and for which the identifier scheme is evident, that all that is required. If the identifier scheme is not well known, or the address of a separate resolve must be used to resolve the identifier, use the schema.org PropertyValue to provide additional information. The propertyID specifies the identifier scheme. CDIF recommends using scheme identifiers from [https://registry.identifiers.org/registry/](https://registry.identifiers.org/registry/). The sdo:value provides the identifier as a string value. If the identifier can be resolved on the web, the sdo:url provides a resolvable URL. 

-   Agent. This pattern is for specifying an Agent in the PROV sense: An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent\'s activity. Agents can be persons, organizations, or software-defined actors. Agents have a name for human recognition, a type (Person, Organization), an identifier, contactPoint and affiliation. Machine agent contact points should be the accessible human who operations the environment running the machine agent. This pattern is used for hard-typed roles in the CDIF implementation- creator, maintainer, contributor, provider. Other roles can be documented using the [schema.org role pattern](http://blog.schema.org/2014/06/introducing-role.html) in the sdo:contributor property. 

-   DistributionObject {contentUrl, encodingFormat, dcterm:conformsTo, distributionAgent }. This pattern specifies information for implementing machine access to a DigitalObject. Includes a URL (contentUrl) for the web location at which the DigitalObject can be accessed, the specifications or profiles to which the serialization and content of the object conform using the Dublin Core conformsTo property, the format of the digital object content (sdo:encodingFormat), and the  the Agent responsible for the distribution platform (provider). This agent is the contact point if there are problems accessing the distributed digitalObject.

---
### Source Document: metadata/archive/schemaorgimplementationTable.md

# Implementation of metadata content items

The following table maps the metadata content items described in the [Metadata Content Requirements](./contentmodel.md) section to the schema.org JSON-LD keys to use in metadata serialization. Some example metadata documents follow. The \'Obl.\' column specifies the cardinality obligation for the property; \'1\' means one value required; 1..\* means at least one value is required; 0..\* means the property is optional and more that one value can be provided. Properties with path from "subjectOf" describe the metadata.


<table>
  <tr>
    <th><b>CDIF content item</b></th>
    <th><b>Obl.</b></th>
    <th><b>Schema.org implementation</b></th>
    <th><b>Scope note</b></th>
  </tr>
  <tr>
    <td>Metadata identifier</td>
    <td>1</td>
    <td>"subjectOf"/"@id":{URI} or "@id":{uri} in node with "identifier":"@id" of the node containing the resource description</td>
    <td>The URI for the metadata record should be the \@id value for the 'subjectOf' element in the JSON instance document tree or "@id":{uri} in a separate graph node with "identifier":"@id" of the node containing the resource description</td>
  </tr>
  <tr>
    <td>Resource identifier</td>
    <td>1</td>
    <td>"identifier":{URI}</td>
    <td>The URI for the resource that is the subject of the metadata record should be the "identifier": value for the root of the JSON instance document tree</td>
  </tr>
  <tr>
    <td>Title</td>
    <td>1</td>
    <td>"name":{string}</td>
    <td>A set of words that should uniquely identify the described resource for human use, in the scope of the metadata catalog containing this metadata record.</td>
  </tr>
  <tr>
    <td rowspan="2">Distribution</td>
    <td>1</td>
    <td>"url":{URL}</td>
    <td>If metadata is about a single digital object</td>
  </tr>
  <tr>
    <td></td>
    <td>"distribution": <br> { "@type": "DataDownload", <br> "contentURL": {URL },\... }</td>
    <td>If the metadata is about an abstract, non-digital, or physical resource that has multiple distributions, with different URL, encodingFormat, conformsTo properties. Each distribution is considered a distinct digital object. The dataDownload MUST include the contentURL, and SHOULD include encodingFormat, dcterms:conformsTo to specify the media type and specification or profile documenting the specific serialization conventions for the download content.</td>
  </tr>
  <tr>
    <td>Rights</td>
    <td>1..*</td>
    <td>"license":{text or URI} <br> Or <br> "conditionsOfAccess":{text or URI}</td>
    <td>URL to license document or text explanation of restrictions on use. There might be multiple links to documents specifying related security, privacy, usage, sharing, etc... concerns.</td>
  </tr>
  <tr>
    <td>Metadata profile identifier</td>
    <td>1</td>
    <td>"subjectOf"/"dcterms:conformsTo": {identifier}</td>
    <td>Use Dublin Core terms property. The value for Base CDIF metadata is 'CDIF_basic_1.0' [tbd; this should be a PID]. Different profiles extending this must define unique identifier strings to use here. Note that the schema.org schemaVersion is used to indicate the version of the schema.org vocabulary, but in general this is not needed for CDIF.</td>
  </tr>
  <tr>
    <td>Metadata date</td>
    <td>0..1</td>
    <td>"subjectOf"/"dateModified":{Date or DateTime}</td>
    <td>Use ISO8601 format. The most recent update date for the metadata content. Harvesters use this to determine if they have already harvested and processed this record.</td>
  </tr>
  <tr>
    <td>Metadata contact</td>
    <td>0..1</td>
    <td>/ "subjectOf"/"maintainer":{Person or Organization}</td>
    <td>Should include a name and contact point (institutional e-mail is best) for the agent responsible for metadata content. This is the contact point to report problems with metadata content. Person and Organization are Agent objects with various properties.</td>
  </tr>
  <tr>
    <td rowspan="2">Resource type</td>
    <td>1</td>
    <td>"@type":{schema.org type}</td>
    <td>Use the most specific [Schema.org resource type](https://schema.org/docs/full.html) that is applicable. Multiple value can be provided but they must be logically consistent.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"additionalType": [{DefinedTerm or URI}, ...]</td>
    <td>If a more specific resource type needs to be specified, add a text or URI value here that identifies the type. MUST be consistent with the \@type. To simplify parsing, always encode as an array.</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>0..1</td>
    <td>"description": {string}</td>
    <td>Free text, with as much detail as is feasible</td>
  </tr>
  <tr>
    <td>Originators</td>
    <td>0..*</td>
    <td>"creator" : [{Person or Organization}, ...]</td>
    <td>The value is a schema.org person or organization. To simplify parsing, always encode as an array. Use ORCID or other PID to identify person or organization where possible</td>
  </tr>
  <tr>
    <td>Publication Date</td>
    <td>0..1</td>
    <td>"datePublished" : {date time}</td>
    <td>Date on which the resource was made publicly accessible. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>Modification Date</td>
    <td>1</td>
    <td>"dateModified" : {date time}</td>
    <td>Date of most recent update to resource content. If Publication date is not provided, defaults to the Modification Date. Use ISO 8601 format.</td>
  </tr>
  <tr>
    <td>GeographicExtent (named place)</td>
    <td>0..*</td>
    <td>"spatialCoverage": { "@type": "Place",<br>"name": {string} or {schema:DefinedTerm} }</td>
    <td>To specify location with place names; if the names are from a gazeteer, use the schema:DefinedTerm to provide a name, identifier, and inDefinedTermSet to fully document the concept.</td>
  </tr>
  <tr>
    <td>GeographicExtent (bounding box)</td>
    <td>0..1</td>
    <td>"spatialCoverage": { <br>"@type": "Place",<br> "geo": {  "@type": "GeoShape", <br> "box": "39.3280 120.1633 40.445  123.7878"   } }</td>
    <td>For bounding box specification of the spatial extent of resource content. See [ESIP SOSO for details](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes). Recommend including only one bounding box; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
  </tr>
  <tr>
    <td>GeographicExtent (curvilinear trace)</td>
    <td>0..1</td>
    <td>"spatialCoverage": { <br>"@type": "Place",<br> "geo": {  "@type": "GeoShape", <br> "line": "39.33 120.77 40.44 123.96 41.00 121.34"   } }</td>
    <td>For resource related to a linear trace like a ship track or airplane flight line</td>
  </tr>
  <tr>
    <td>GeographicExtent (point location)</td>
    <td>0..1</td>
    <td>"spatialCoverage": {<br> "@type": "Place", <br>"geo": {  "@type":  "GeoCoordinates",  <br> "latitude": 39.3280,   <br>  "longitude": 120.1633 } }</td>
    <td>For a point location specification of the spatial extent of resource content. Recommend including only one point; behavior of harvesting clients when multiple geometries are specified is unpredictable.</td>
    </tr>
  <tr>
    <td>GeographicExtent (other serialization)</th>
    <td>0..*</th>
    <td>"geosparql:hasGeometry": { <br> "@type": "sf#Point", <br> "geosparql:asWKT":  "@type":#wktLiteral", <br>"@value":"POINT(-76  -18)"},<br> "Geosparql:crs": {"@id":"CRS84"} }</th>
    <td>Optional geographic extent using other more interoperable geometries, GeoSPARQL us recommended, see <a href="https://book.oceaninfohub.org/thematics/spatial/README.html#simple-geosparql-wkt">Ocean InfoHub</a>. (Note URIs in example are truncated...) Other geometry schemes might be specified in a specific domain profile, e.g. for atmospheric, subsurface data, or local coordinate systems.</th>
  </tr>
  <tr>
    <td rowspan="2">Distribution Agent</td>
    <td>0..*</td>
    <td>"provider":{Person or Organization}</td>
    <td>Contact point for the provider of a distribution. For a simple digital object with a download URL, or a resource with multiple distributions all from the same provider.</td>
  </tr>
  <tr>
    <td>0..*</td>
    <td>"distribution": [ { "@type": "DataDownload","provider":{Person or Organization} }...]</td>
    <td>If there are multiple distributions with different providers, each distribution can have a separate provider</td>
  </tr>
  <tr>
    <td>Variable (PropertyValue)</td>
    <td>0..*</td>
    <td>"variableMeasured":<br> [ { "@type":"PropertyValue",<br>&emsp; "@id": "astm:var0011",<br>&emsp;  "propertyID": [ "pato:PATO_0000025",<br>&emsp;&emsp;&emsp;"astm:prop/0405" ],<br>&emsp;  "name": "hostMineral", <br>&emsp; "description": "...." }...]</td>
    <td>Follow <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables">ESIPfed Science on Schema.org recommendation</a>, see also discussion for representing more complex data structures in <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Experimental.md#AdvancedVariableValueType">ESIPfed Experimental</a> and the <a href="https://cross-domain-interoperability-framework.github.io/cdifbook/data_integration/ddidescriptiondatastructure.html">Data Integration module of CDIF</a>. Variable must have a name and description, should have a propertyID with URI for the represented concept. The URI in the propertyID provides the semantic linkage for meaning of the variable.</td>
  </tr>
  <tr>
    <td>Variable (StatisticalVariable)</td>
    <td>0..*</td>
    <td>"variableMeasured":<br> [ { "@type":"StatisticalVariable",<br> "@id": "astm:var0011",<br>"@type": "StatisticalVariable",<br>
&emsp;"measuredProperty":<br>
&emsp;&emsp;{"@type":"Property",      &emsp;&emsp;"identifier":"astm:id/305978",<br>
&emsp;&emsp;"name":"Average age"}]</td>
    <td>Statistical variable offers properties useful for describing social science statistical variables like populationType and statType. Use of StatisticalVariable is preferred for variables with values calculated from some aggregation process.</td>
  </tr>
  <tr>
    <td>Keyword</td>
    <td>0..*</td>
    <td>"keywords":<br>[ {string}, <br> {"@type":"DefinedTerm", <br> "name": "OCEANS", <br> "inDefinedTermSet": "gcmd:sciencekeywords", <br> "identifier": "gcmd:concept/916b....6167d" },...]</td>
    <td>Implement with text for tags, and schema:DefinedTerm for keywords from a controlled vocabulary. The DefinedTerm approach is used to represent concepts.</td>
  </tr>
  <tr>
    <td rowspan="5">Temporal coverage</td>
    <td rowspan="5">0..*
    </td>
    <td colspan="2">Temporal coverage can be expressed in several ways: a calendar/clock dateTime or date time interval using ISO8601 serialization, a named time ordinal era, an interval bounded by time ordinal era, or with a numeric coordinate in a temporal reference system.</td>
  </tr>
  <tr>
    <td>"temporalCoverage": "2018-01-22"</td>
    <td>Calendar data or clock time instant use ISO8601 encoding</td>
  </tr>
  <tr>
    <td>"temporalCoverage": "2012-09-20/2016-01-22"</td>
    <td>Calendar data or clock time interval use ISO8601 encoding</td>
  </tr>
  <tr> 
    <td>"temporalCoverage": <br> [{ "@type":"time:ProperInterval", <br> "time:intervalStartedBy": "isc:LowerDevonian, <br>  "time:intervalFinishedBy": "isc:LowerPermian" }]</td>
    <td>Time ordinal era interval, use owl:time namespace, time: http://www.w3.org/2006/time#. This example uses <a href="http://resource.geosciml.org/classifier/ics/ischart/">International chronostratigraphic chart, isc</a>. See <a href="https://perio.do/en/">PeriodO</a> for identifiers for many other named time intervals.</td>
  </tr>
  <tr>
    <td>"temporalCoverage": <br> [{ "time:ProperInterval- 345/298 Ma" }]</td>
    <td>For time interval specified using geologic ages, in Ka, Ma or Ga; The text string is an abbreviated owl time interval (proposal, under discussion)</td>
  </tr>
  <tr>
    <td>Related agents (contributor role)</td>
    <td>0..*</td>
    <td>"contributor": [ {Person or Organization}, ... ]</td>
    <td>Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators.</td>
  </tr>
  <tr>
    <td>Related agent (other role)</td>
    <td></td>
    <td>"contributor": {"@type": "Role", <br>&emsp; "roleName": "Principal Investigator",<br>&emsp;"contributor": {"@type": "Person",&emsp;&emsp;"@id": "https://orcid.org/...",<br>&emsp;&emsp;"name": "John Doe",<br>&emsp;&emsp;"affiliation": {"@type": "Organization",<br>&emsp;&emsp;&emsp;"@id": "https://ror.org/...",<br>&emsp;&emsp;&emsp;"name": "..."},<br>&emsp;&emsp;"contactPoint": {"@type": "ContactPoint",<br>&emsp;&emsp;&emsp;"email": "john.chodacki@ucop.edu"}</td>
    <td>To assign roles to contributors like editor, maintainer, publisher, point of contact, copyright holder  (e.g.  DataCite contributor types), use the rather convoluted <a href="http://blog.schema.org/2014/06/introducing-role.html">role construction defined by schema.org</a></td>
  </tr>
  <tr>
    <td>Related resources</td>
    <td>0..*</td>
    <td>"relatedLink": [{"@type":"LinkRole", "linkRelationship": "...",<br>"target: {"@type": "EntryPoint", <br> "encodingType": "text/html",<br>"name": "...",<br>"url": "https://example.org/data/stations" } } ]</td>
    <td>Use schema.org relatedLink with a LinkRole value, and the link URL in a 'target' EntryPoint object. These properties expect WebPage and Action as their domain, so the <a href="https://validator.schema.org/">schema.org validator</a> will throw a warning (not an error). Related resource links are useful for evaluation and use of data, but because of the wide variety of relationship possibilities, difficult to use in general search scenarios. Use a soft-type implementation, with a link relationship type using a schema:DefinedTerm, and a resolvable identifier for the relationship target.</td>
    </tr>
  <tr>
    <td>Funding</th>
    <td>0..*</th>
    <td>"funding" :<br> { "@id": "URI for grant", <br> "@type": "MonetaryGrant",<br> "identifier": "grant id",  <br> "name": "grant title", <br> "funder":<br> { "@id": "ror for org", <br> "@type": "Organization", <br>  "name": "org name",  <br> "identifier": [ "other identifiers" ] } }</th>
    <td>Use schema.org encoding and <a href="https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#funding">science on schema.org pattern</a>. Other organization properties can be included in the funder/Organization.</th>
  </tr>
  <tr>
    <td>Policies</td>
    <td>0..*</td>
    <td>"publishingPrinciples": [ {"@type": "CreativeWork"}.... ]</td>
    <td>FDOF digitalObjectMutability, RDA digitalObjectPolicy, FDOF PersistencyPolicy. Policies related to maintenance, update, expected time to live.</td> </tr>
<tr> <td> Checksum  </td><td> 0..1  </td><td> "distribution\": \[ { \"@type\": \"DataDownload\",    \"spdx:checksum\": {<br>&nbsp;&nbsp;"spdx:algorithm":"string",<br>&nbsp;&nbsp; "spdx:checksumValue":"string" },..  }\...\]  </td>
<td>A string value calculated from the content of the resource representation, used to test if content has been modified. No schema.org property, follow DCAT v3 adoption of [Software Package Data Exchange (SPDX)](https://spdx.org/rdf/terms/) property; The [spdx Checksum object](https://spdx.org/rdf/spdx-terms-v2.1/classes/Checksum___-238837136.html) has two properties: algorithm and checksumValue. The checksum is a property of each distribution/DataDownload. </td></tr>
<tr >
<td colspan="4"><b>Provenance for discovery</b> is limited to documenting technology used in the creation of the dataset and documening other datasets (datasets) that were inputs to the content of the described resource.</td></tr>
<tr><td>Provenance (instruments, software etc.) </td><td>0..* </td><td>   "prov:wasGeneratedBy": {
        "@type": "prov:Activity",
        "prov:used": [
            "nerc:collection/L05/current/134",
            "nerc:collection/B76/current/B7600031" ]
 },</td><td>Identify sensors, instruments, platforms, software, algorithms etc. used in the creation of the described resource</td></tr>
    <td>Provenance (input datasets) </td><td>|0..* </td><td>   
    "prov:wasDerivedFrom": [<br>
        "http://doi.org/10.547/347848",
        "http://doi.org/10.3578/h5ls",
        "http://doi.org/10.547/93578" ],</td><td>"</td></tr>
<tr>
<td colspan="4"><b>Quality information for discovery</b>: A text statement documenting quality of the resource should be included in the   sdo:description. If there are quality policies or certificates that apply, these should be specified in the sdo:policies. Quality measurement or assessment protocols that have an output result specific to this resource can be specified using dqv:hasQualityMeaurement </td>
</tr><tr>
<td>Quality measure</td><td>0..*</td><td>"dqv:hasQualityMeasurement": [<br> {
"@type": "dqv:QualityMeasurement",<br>
&emsp;"dqv:isMeasurementOf": &emsp;&emsp;&nbsp;&nbsp;"nerc:collection/L27/current/ARGO_QC",
&emsp;&emsp;"dqv:value": "good" },<br>
        { "@type": "dqv:QualityMeasurement",
&emsp;&emsp;"dqv:isMeasurementOf":<br>&emsp;&emsp; "imf:dsbb/2003/eng/dqaf.htm",
&emsp;&emsp;"dqv:value":<br>
&emsp;&emsp;"http://linkToASpecificQualityReport" }]
</td><td>Quality assesment or measument conducted using procedure or protocol specified by the dqv:isMeasurementOf property, with result value specified in the dqv:value property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment.</td>
</tr>
        </table>

---
### Source Document: metadata/contentmodel.md

# Basic discovery metadata content model

The core of the CDIF profile for resource discovery is a set of implementation-independent content requirements that specify the required information to support a basic level of discovery interoperability for resources of any type.  The following list includes the minimum required content for basic resource description, discovery, and access. This recommendation is a synthesis of various metadata schemes, including ISO 19115-1:2014, schema.org conventions from ESIPFed Science on Schema.org and Ocean Data net, DCAT, DCAT-AP, and [FDO Kernel Attributes-2.0](https://docs.google.com/document/d/1OF49wTNVuv-6OXlNerhBTqVtHyc7jutTaUHjn6BZCs0). A mapping between these various schemas and CDIF content elements is available in [Metadata mappings](mapping.md). Note that these content requirements are scoped for a broad spectrum of resource types. It is expected that other fields will need to be added in extensions for specific kinds of resources.

## Required
If the content of a required element does not provide useful information, the metadata is considered useless for even the most rudimentary discovery use cases. Conformant metadata MUST provide valid values, i.e., a meaningful title that identifies the resource, either a URL or text statement of how to obtain the resource, a statement of any licensing, usage, or access constraints (i.e., Rights), and identifiers for the specification of the metadata serialisation and the type of the resource described.

- **Resource identifier** (1 entry): A globally unique, resolvable identifier for the resource described by the metadata record.
- **Title** (1 entry): Succinct (preferably &lt;250 characters) name of the resource; should be sufficient to uniquely identify the resource for a human user.
- **Distribution**: URL, Distribution object, or Access Instructions (1 entry): If the resource is a digital object accessible online, provide a URL that will retrieve the resource. If the resource has multiple representations, provide a Distribution Object documenting the various options with a URL and representation profile for each. Metadata for distributions through an API that allows query, filter, or processing as part of a data access request are described in the Queryable Distribution Interfaces (API) section, below. If the resource is not accessible online, provide a URL to a landing page used to access the resource, or minimally, provide a text description explaining how to access the resource in the metadata (Access Instructions).
- **Rights** (1 to many entry): Information about required access permissions, licences, contractual requirements, use constraints, and security constraints. Might be described in text or through links to external documents. (See 6.4. Data Access for providing machine-actionable rights descriptions.)
- **Metadata profile identifier** (1 to many): Identifier for metadata specification (profile) used to create this metadata record. Generally this will be populated automatically if the metadata is created using CDIF aware tools.
- **Resource type** (1 to many): A scoped name (label with classification scheme) that specifies the kind of resource described by the metadata. The resource type might be used to determine validation requirements specific to descriptions for that kind of resource.

## Conditional elements
These are content elements for which every resource should have useful information, but for which the information may not be applicable for some kinds of resources. 

- **Variable** (0 to many entries): Required for datasets. The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be, ideally, qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text. Variable metadata should include as much content as needed for users to understand the type of the variable (e.g. measured, statistically derived, or simulated), its units, and any relevant reference systems for its values (see [Universals](../universals/univintro.md) ). Details of data structure and schema more closely related to interoperability, data integration, and usage than to data discovery are discussed in [Data Description for Integration](../data_description/datadescriptionforintegration.md).
- **Temporal Coverage** (0..1 entry) Required if resource content is specific to some time interval. The time interval represented by or the subject of the described resource. This could be the time interval when data were collected, or an archaeological or geological time interval that is the subject of the resource. Need to account for clock time, calendar time (Gregorian, Julian, Hebrew, Islamic, Chinese, Mayan...), cyclical time (summer, first quarter, mating season, new moon, pay day) and for named time ordinal eras (Jurassic, Younger Dryas, Early Minoan I, Late Stone Age). See [OWL Time](https://www.w3.org/TR/owl-time/).
- **Geographic Extent** - (0..many)  Required if resource has a geographic extent for its subject, either a named location, bounding rectangle, linear trace, or point. To support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 8486 datum. There are various other systems for describing location (see [Space](../universals/univgeography.md) ); these can be provided as alternate location descriptions, recognizing that they might be meaningful to some metadata harvesting agents. Some resources may not be usefully described by a WGS 84 extent, in which case indicate nil:notapplicable; this would include extraterrestrial resources.
  - *Bounding Rectangle*: North Bounding Latitude, South Bounding Latitude, East Bounding Longitude, West Bounding Longitude. The minimum rectangle that completely contains the coverage extent for the resource content. Coordinate order and syntax are determined by the serialisation profile.
  - *Linear trace*: a linear trace e.g. of a ship's track, aircraft flight path, or surface traverse, represented as a series of points. Coordinate order and syntax are determined by the serialisation profile.
  - *Point*: Latitude, Longitude. A centroid point for the coverage extent of the resource, or the location of the resource content if a point location is appropriate. Coordinate order and syntax are determined by the serialisation profile.
  - *Named location*: Place name referenced to some gazetteer. Use scoped name pattern {label, authority, optional identifier}.
  
## Recommended
Other properties that should be specified if possible and relevant. All are optional.
- **Description** (0..1 entry): Inform the reader about the resource's content, context, provenance, and any other information deemed useful for future cross-domain usage. SHACL validation will throw warning if not present.
- **Originators** (0 to many entries): One or more parties (person or organisation) that have a role related to the origin of the resource, e.g., author or editor. Each party has a name (label), identifier, and optional contact information. SHACL validation will throw warning if not present.
- **Modified Date** (0..1 entry): Date (not temporal extent) when the most recent changes to the resource were completed. Use a "year" or [ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601) format. Alternative date formatting must be machine-readable and consistent across all datasets. SHACL validation will throw warning if not present.
- **Distribution Agent** (0..1 entry):The party (person or organisation) to contact about accessing the resource. Each party has a name (label), identifier, and optional contact information. If there are multiple distribution options with different contact points, the Distribution Agent should be specified as part of the Distribution Object.
- **Checksum**. (0 or 1): A string value calculated from the content of a digital object that allows verification that the content of the object has not been modified. Even insignificant changes to the content of the file will change its checksum. The algorithm used to calculate the checksum must be documented. See also [RFC-6920 'Naming things with hashes'](https://www.rfc-editor.org/rfc/rfc6920.html) that establishes ways to identify checksum algorithms and to represent checksum values as a URI. Note that checksums apply to specific digital objects, typically a unique resource representation. Non-digital resources do not have checksums; their representations can have checksums. See implementation notes in Appendix 1.
- **Funding**. (0 to many entries): Cite funding sources (Grants, contracts...). Each source has a grant or contract identifier, source organisation, and label.
- **Keyword** (0 to many entries): Distinguish 'tags' and 'controlled terms'. Tags are simply words that a metadata creator thinks will be useful for users to identify resources of interest. Controlled terms are words defined in a vocabulary that minimally include the word (a fixed string to identify the term for humans) and a definition. Each term represents some concept. More semantically rich vocabularies would include resolvable identifiers, source information, and links to related terms (see [Cox et al., 2021](https://doi.org/10.1371/journal.pcbi.1009041) ). One common set of relationships in a vocabulary is a kind-of hierarchy linking broader to narrower concepts. Controlled terms should minimally be represented with a label and scheme name that identifies the source vocabulary; ideally a term URI and scheme URI could be included for more accurate identification and data integration. 
- **Policies** (0 to many entries): Policies used in management of the described resource, including whether the content may be changed (mutable or immutable), any scheduled updates, what is the expected lifetime for resource availability, what (if any) is the maintenance schedule, versioning, documentation for changes and change requests. Explicit support for specific policy frameworks can be included (e.g., CARE).
- **Publication Date** (0 or 1): Date (not temporal extent) when the resource was made accessible. Use a ‘year’ or ISO 8601 date and time format. Alternative date formatting must be machine-readable and consistent across all datasets. If no publication date is known, estimate the publication date range, enter the oldest year as the publication date, and include the estimated date range in the Description field.
- **Other related agents** (0 to many entries): Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators. Includes a variety of roles like maintainer, publisher, point of contact, copyright holder, contributor (see e.g. [DataCite contributor types](https://datacite-metadata-schema.readthedocs.io/en/4.5_draft/properties/recommended_optional/property_contributor.html#a-contributortype), [ISO19115-1 role code](https://wiki.esipfed.org/ISO_19115_and_19115-2_CodeList_Dictionaries#CI_RoleCode) )
- **Related resources** (0 to many entries): Links to related data, publications, annotation, data sources, software used, etc. Links have at least a label, relationship type, and resolvable target resource identifier.
- **Version** (0 or 1): If the resource is versioned, specify the label for this version. Version labels should follow a scheme that allows alphanumeric sorting reflecting the order of version release.
- **Provenance** (0..many): For discovery, provide information about datasets that were used in the creation of the described resource and specify sensors, platforms, software, algorithms etc. used to aquire information contained in the resource.  Details about workflows, activity sequences, association of sensors etc. with specific variables, individuals associate with particular activities in workflow etc. require used of cdif prov extension (TBD).
- **Quality** (0..many) Provide statements about the quality of information in the described resource,  information about quality policies or certificates that apply to the resource, and results of quality measures with information about the measurement protocol/procedure used. In all cases the focus should be on information useful for initial assessment by potential users.

## Properties for metadata management
These elements provide information for the operation of a distributed catalogue system with harvesting of metadata between catalogue servers. Values should be populated automatically by metadata creation tools, requiring no user input.  Some providers might not include this information in metadata interchange files. 
- **Metadata Date** (0..1 entry): Last metadata update/creation date-time stamp in ISO 8601 date and time format. This may be automatically updated on metadata import if a metadata format conversion is necessary.
- **Metadata Contact Agent** (0..1 entry): The party responsible for metadata content and accuracy; Agent object includes a name (label), identifier, and optional contact information
- **Metadata Identifier** (0..1 entry): The identifier for the Digital object that contains the metadata.



---
### Source Document: metadata/core.md

# Core Profile

Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/cdifCoreStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/CDIFCoreImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/coreRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/cdifCore-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCore/index.html)

The core of the Cross Domain Interoperability Framerwork is a set of implementation-independent content that must be specified in any CDIF-conformant metadata. This core set is supplemented by a more extensive set of metadata properties that are expected to apply to any information resource of interest, but are optional in the model. These optional properties might not be applicable in some situations or, more commonly, are unknown, not available, or not provide for some reason. 

 This recommendation is a synthesis of various metadata schemes, including ISO 19115-1:2014, schema.org conventions from [ESIPFed Science on Schema.org](https://github.com/ESIPFed/science-on-schema.org) and Ocean Data net, DCAT, DCAT-AP, and [FDO Kernel Attributes-2.0](https://docs.google.com/document/d/1OF49wTNVuv-6OXlNerhBTqVtHyc7jutTaUHjn6BZCs0). These core content requirements are scoped for a broad spectrum of resource types; other fields will be added in the CDIF extension profiles.

## Information Model

 ### Required
If the content of a required element does not provide useful information, the metadata is considered useless for even the most rudimentary discovery use cases. Conformant metadata MUST provide valid values: an identifier for the described resource, a meaningful title that identifies the resource, either a URL or Distribution object (details later) that enables access to the resource, a statement of any licensing, usage, or access constraints (i.e., Rights),  an identifier for the type of resource described in the metadata, and identifier(s) for the specification of the metadata serialisation.

- **Resource identifier** (1 entry): A globally unique, resolvable identifier for the resource described by the metadata record.
- **Title** (1 entry): Succinct (preferably &lt;250 characters) name of the resource; should be sufficient to uniquely identify the resource for a human user.
- **Distribution**: URL, Distribution object, or Access Instructions (1 entry): There are several options. If the resource is a single digital object accessible online, provide a URL that will retrieve the resource. If the resource has multiple representations, or to provide users more information about the resource representation, a Distribution Object should be used to document the various possible representations and component files with a URL  for each. Metadata for distributions through an API that allows query, filter, or processing as part of a data access request are described in the Queryable Distribution Interfaces (API) section, below. If the resource is not accessible online, provide a URL to a landing page that describes how to access the resource.
- **Rights** (1 to many entry): Information about required access permissions, licences, contractual requirements, use constraints, and security constraints. Might be described in text or through links to external documents. 
- **Resource type** (1 to many): A scoped name (label with classification scheme) that specifies the kind of resource described by the metadata. The resource type might be used to determine validation requirements specific to descriptions for that kind of resource.
- **Metadata profile identifier** (1 to many): Identifier for metadata specification (profile) used to create this metadata record. Generally this will be populated automatically if the metadata is created using CDIF aware tools.

### Recommended
Other properties that should be specified if possible and relevant. All are optional.
- **Description** (0..1 entry): Inform users about the resource's content, context, provenance, and any other information deemed useful for future cross-domain usage. 
- **Originators** (0 to many entries): One or more parties (person or organisation) that have a role related to the origin of the resource, e.g., author or editor. Each party has a name (label), identifier, and optional contact information. 
- **Modified Date** (0..1 entry): Date (not temporal extent) when the most recent changes to the resource were completed. Use [ISO 8601 date and time](https://en.wikipedia.org/wiki/ISO_8601) format. Alternative date formatting must be machine-readable and consistent across all datasets. 
- **Distribution Agent** (0..1 entry):The party (person or organisation) to contact about accessing the resource. Each party has a name (label), identifier, and optional contact information. If there are multiple distribution options with different contact points, the Distribution Agent should be specified as part of the Distribution Object.
- **Checksum**. (0 or 1): A string value calculated from the content of a digital object that allows verification that the content of the object has not been modified. Even insignificant changes to the content of the file will change its checksum. The algorithm used to calculate the checksum must be documented. See also [RFC-6920 'Naming things with hashes'](https://www.rfc-editor.org/rfc/rfc6920.html) that establishes ways to identify checksum algorithms and to represent checksum values as a URI. Note that checksums apply to specific digital objects, typically a unique resource representation. Non-digital resources do not have checksums; their representations can have checksums. See implementation notes in Appendix 1.
- **Funding**. (0 to many entries): Cite funding sources (Grants, contracts...). Each source has a grant or contract identifier, source organisation, and label.
- **Keyword** (0 to many entries): Distinguish 'tags' and 'controlled terms'. Tags are simply words that a metadata creator thinks will be useful for users to identify resources of interest. Controlled terms are words defined in a vocabulary that minimally include the word (a fixed string to identify the term for humans) and a definition. Each term represents some concept. More semantically rich vocabularies would include resolvable identifiers, source information, and links to related terms (see [Cox et al., 2021](https://doi.org/10.1371/journal.pcbi.1009041) ). One common set of relationships in a vocabulary is a kind-of hierarchy linking broader to narrower concepts. Controlled terms should minimally be represented with a label and scheme name that identifies the source vocabulary; ideally a term URI and scheme URI could be included for more accurate identification and data integration. 
- **Policies** (0 to many entries): Policies used in management of the described resource, including whether the content may be changed (mutable or immutable), any scheduled updates, what is the expected lifetime for resource availability, what (if any) is the maintenance schedule, versioning, documentation for changes and change requests. Explicit support for specific policy frameworks can be included (e.g., CARE).
- **Publication Date** (0 or 1): Date (not temporal extent) when the resource was made accessible. Use a ‘year’ or ISO 8601 date and time format. Alternative date formatting must be machine-readable and consistent across all datasets. If no publication date is known, estimate the publication date range, enter the oldest year as the publication date, and include the estimated date range in the Description field.
- **Other related agents** (0 to many entries): Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators. Includes a variety of roles like maintainer, publisher, point of contact, copyright holder, contributor (see e.g. [DataCite contributor types](https://datacite-metadata-schema.readthedocs.io/en/4.5_draft/properties/recommended_optional/property_contributor.html#a-contributortype), [ISO19115-1 role code](https://wiki.esipfed.org/ISO_19115_and_19115-2_CodeList_Dictionaries#CI_RoleCode) )
- **Related resources** (0 to many entries): Links to related data, publications, annotation, data sources, software used, etc. Links have at least a label, relationship type, and resolvable target resource identifier.
- **Version** (0 or 1): If the resource is versioned, specify the label for this version. Version labels should follow a scheme that allows alphanumeric sorting reflecting the order of version release.
- **Provenance** (0..many): For discovery, provide information about datasets that were used in the creation of the described resource and specify sensors, platforms, software, algorithms etc. used to aquire information contained in the resource.  Details about workflows, activity sequences, association of sensors etc. with specific variables, individuals associate with particular activities in workflow etc. require used of cdif prov extension (TBD).


### Properties for metadata management
These elements provide information for the operation of a distributed catalogue system with harvesting of metadata between catalogue servers. Values should be populated automatically by metadata creation tools, requiring no user input.  Some providers might not include this information in metadata interchange files. 
- **Metadata Date** (0..1 entry): Last metadata update/creation date-time stamp in ISO 8601 date and time format. This may be automatically updated on metadata import if a metadata format conversion is necessary.
- **Metadata Contact Agent** (0..1 entry): The party responsible for metadata content and accuracy; Agent object includes a name (label), identifier, and optional contact information
- **Metadata Identifier** (0..1 entry): The identifier for the Digital object that contains the metadata.

## Implementation

The current recommended implementation uses the schema.org vocabulary, with a few entities and properties from other vocabularies to fill gaps; see [Implementation of metadata content items](coreSchemaImplementationNew.md). For background on JSON, JSON-LD and general implementation patters CDIF is using, see [Schema.org implementation notes](schemaOrgImplementationpatterns.md).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/coreSchemaImplementationNew.md

# CDIF Core Profile — Schema.org Implementation

This page documents the mapping between CDIF content items and their schema.org implementation. Some example metadata documents are accessible in the [Core Github repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/tree/main/examples). The \'Obl.\' column specifies the cardinality Cardinality for the property; \'1\' means one value required; 1..\* means at least one value is required; 0..\* means the property is optional and more that one value can be provided. Properties with path from "subjectOf" describe the metadata.

All property names use namespace prefixes as declared in the `@context` (e.g. `schema:`, `dcterms:`). The `schema:` prefix is required for all schema.org properties. The CDIF JSON-LD implementation uses a hierarchical JSON structure, and CURIE syntax to abbreviate URIs using prefixes defined in the JSON-LD context.  The implementation does not map un-prefixed JSON keys to URIs, rather prefixes a namespace abbreviation on the key label to represent the URI.  This enables using standard JSON schema to validate documents and avoids confusion about the vocabulary origin of keys used in the JSON.

Each item lists its Cardinality, JSON encoding, and a Description explaining usage. 

See also [graphical presentation of the core profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCore/index.html)

Artefacts for the core profile are in this [Github repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/tree/reviewRevision202606) (TBD--update link to release tag)


## Metadata identifier
- **Cardinality:** mandatory
- **JSON:** `"schema:subjectOf" / "@id": "{URI}"`
- **Description:** The URI for the metadata record should be the `@id` value for the `schema:subjectOf` node. This node has `@type ["schema:Dataset"]` with `schema:additionalType ["dcat:CatalogRecord"]`, and a `schema:about` property referencing the `@id` of the root resource node.

## Resource identifier
- **Cardinality:** mandatory
- **JSON:** `"schema:identifier": {PropertyValue or string}`
- **Description:** The primary identifier for the resource. Can be a simple string (ideally a resolvable URI), or a `schema:PropertyValue` with `propertyID` (identifier scheme, e.g. from [identifiers.org](https://registry.identifiers.org/registry/)), `value` (the identifier string), and `url` (resolvable link). The PropertyValue approach is strongly recommended following the [ESIP Science on Schema.org guidance](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#identifier).

## Title
- **Cardinality:** mandatory
- **JSON:** `"schema:name": {string}`
- **Description:** A set of words that should identify the described resource for human use. Ideally, should be unique in the scope of the metadata catalog containing this metadata record.

## Distribution
- **Cardinality**: mandatory.*Either a `schema:url` or a `contentUrl` inside `schema:distribution` is required to indicate how to get the resource*.
- *Landing page URL*
  - **JSON:** `"schema:url": {URL}`
  - **Description:** This URL is generally expected to GET an HTML landing page about the resource.
- *Distribution array*
  - **JSON:**
    ```json
    "schema:distribution": [
      {"@type": ["schema:DataDownload"], "schema:contentUrl": {URL}, ... },
      {"@type": ["schema:WebAPI"], "schema:serviceType": ..., ... }
    ]
    ```
- **Description:** An array of distribution objects. Items may be DataDownload (file-based access) or WebAPI (service-based access). A DataDownload must include `schema:contentUrl`, and should include `schema:encodingFormat` and `dcterms:conformsTo`. The `@type` is encoded as an array (e.g. `["schema:DataDownload"]`).

## Rights
- **Cardinality:** 1..*
- **JSON:** `"schema:license": [{text or URI or CreativeWork}, ...]` or `"schema:conditionsOfAccess": [{text or URI}, ...]`
- **Description:** At least one of `schema:license` or `schema:conditionsOfAccess` must be provided (as arrays). URL to license document or text explanation of restrictions on use. There might be multiple links to documents specifying related security, privacy, usage, sharing, etc. concerns.

## Metadata profile identifier
- **Cardinality:** 1..*
- **JSON:**
  ```json
  "schema:subjectOf" / "dcterms:conformsTo": [
    {"@id": "https://w3id.org/cdif/core/1.1/"}
  ]
  ```
- **Description:** An array of objects, each with an `@id` property whose value is a conformance URI. For CDIFCore, the core URI is required. Extended profiles add their own conformance URIs to this array.  Note that the CDIF conformance class URIs are registered such that the base URI (e.g. https://w3id.org/cdif/core/1.1/) resolves to this implementation guidance page; add /schema and the uri will resolve to the JSON schema for validating instance documents using that profile; add /shacl and the shacl rules, encoded in turtle format, will be returned.

## Metadata date
- **Cardinality:** 0..1
- **JSON:** `"schema:subjectOf" / "schema:sdDatePublished": {Date}`
- **Description:** Use ISO 8601 format. The most recent publication date for the metadata content. Harvesters use this to determine if they have already harvested and processed this record.

## Metadata contact
- **Cardinality:** 0..1
- **JSON:** `"schema:subjectOf" / "schema:maintainer": {Person or Organization}`
- **Description:** Should include a name and contact point (institutional e-mail is best) for the agent responsible for metadata content. This is the contact point to report problems with metadata content. Person and Organization are Agent objects with various properties.

## Metadata catalog
- **Cardinality:** 0..1
- **JSON:**
  ```json
  "schema:subjectOf" / "schema:includedInDataCatalog": {
    "@type": "schema:DataCatalog",
    "schema:name": ...,
    "schema:url": ...
  }
  ```
- **Description:** Identifies the data catalog or repository containing this metadata record. Value is a `schema:DataCatalog` with at least a name and URL.

## Resource type
- **Primary type — `@type`**
  - **Cardinality:** mandatory
  - **JSON:** `"@type": ["schema:Dataset", ...]`
  - **Description:** An array of schema.org type values using the `schema:` prefix. Must include `"schema:Dataset"`. Additional allowed types: `schema:CreativeWork`, `schema:SoftwareApplication`, `schema:SoftwareSourceCode`, `schema:Product`, `schema:WebAPI`, `schema:DigitalDocument`, `schema:Collection`, `schema:ImageObject`, `schema:DataCatalog`, `schema:DefinedTermSet`, `schema:MediaObject`.
- **Additional type — `schema:additionalType`**
  - **Cardinality:** 0..*
  - **JSON:** `"schema:additionalType": [{DefinedTerm or string}, ...]`
  - **Description:** If a more specific resource type needs to be specified using a vocabulary other than schema.org, add a text or URI value here. Must be consistent with the `@type`. Always encode as an array.

## Description
- **Cardinality:** 0..1
- **JSON:** `"schema:description": {string}`
- **Description:** Free text, with as much detail as is feasible.

## Originators
- **Cardinality:** 0..*
- **JSON:** `"schema:creator": {"@list": [{Person or Organization}, ...]}`
- **Description:** Author or originator of intellectual content. Uses the JSON-LD `@list` construct to preserve author order. Each item can be a Person, Organization, or an object reference (`{"@id": "..."}`) to an agent defined elsewhere. Use ORCID or other PID to identify persons where possible.

## Publication Date
- **Cardinality:** 0..1
- **JSON:** `"schema:datePublished": {date time}`
- **Description:** Date on which the resource was made publicly accessible. Use ISO 8601 format.

## Modification Date
- **Cardinality:** mandatory
- **JSON:** `"schema:dateModified": {date time}`
- **Description:** Date of most recent update to resource content. If Publication Date is not provided, defaults to the Modification Date. Use ISO 8601 format.

## Other identifiers
- **Cardinality:** 0..*
- **JSON:** `"schema:sameAs": [{URI or PropertyValue}, ...]`
- **Description:** Other identifiers for the same resource, as IRI reference strings, object references (`{"@id": "..."}`), or structured identifiers using `schema:PropertyValue`.

## Version
- **Cardinality:** 0..1
- **JSON:** `"schema:version": {string or number}`
- **Description:** The version number or identifier for this resource. Values should sort from oldest to newest using an alphanumeric sort on version strings.

## Language
- **Cardinality:** 0..1
- **JSON:** `"schema:inLanguage": {string}`
- **Description:** The language of the dataset content (e.g. `"en"`, `"fr"`).

## Keyword
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:keywords": [
    {string},
    {
      "@type": "schema:DefinedTerm",
      "schema:name": "OCEANS",
      "schema:inDefinedTermSet": "gcmd:sciencekeywords",
      "schema:identifier": {...}
    },
    ...
  ]
  ```
- **Description:** Implement with text for tags, and `schema:DefinedTerm` for keywords from a controlled vocabulary. The DefinedTerm approach is used to represent concepts with links to their defining vocabulary. Recommend using DefinedTerm for all keywords if any are from a known vocabulary.

## Distribution Agent
- **Single provider**
  - **Cardinality:** 0..*
  - **JSON:** `"schema:provider": [{Person or Organization}, ...]`
  - **Description:** Contact point for the provider of a distribution. For a simple digital object with a download URL, or a resource with multiple distributions all from the same provider.
- **Per-distribution provider**
  - **Cardinality:** 0..*
  - **JSON:** `"schema:distribution": [{"@type": ["schema:DataDownload"], "schema:provider": [{Person or Organization}]}, ...]`
  - **Description:** If there are multiple distributions with different providers, each distribution can have a separate provider array.

## Related agents (contributor role)
- **Cardinality:** 0..*
- **JSON:** `"schema:contributor": [{Person or Organization}, ...]`
- **Description:** Recognition for others who have contributed to the production of the resource but are not recognized as authors/creators.

## Related agent (other role)
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:contributor": [{
    "@type": "schema:Role",
    "schema:roleName": "Principal Investigator",
    "schema:contributor": {
      "@type": "schema:Person",
      "@id": "https://orcid.org/...",
      "schema:name": "John Doe",
      "schema:affiliation": {
        "@type": "schema:Organization",
        "@id": "https://ror.org/...",
        "schema:name": "..."
      },
      "schema:contactPoint": {
        "@type": "schema:ContactPoint",
        "schema:email": "john.doe@example.org"
      }
    }
  }]
  ```
- **Description:** To assign roles to contributors like editor, maintainer, publisher, point of contact, copyright holder (e.g. DataCite contributor types), use the [role construction defined by schema.org](http://blog.schema.org/2014/06/introducing-role.html).

## Related resources
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:relatedLink": [{
    "@type": "schema:LinkRole",
    "schema:linkRelationship": "...",
    "schema:target": {
      "@type": "schema:EntryPoint",
      "schema:encodingFormat": "text/html",
      "schema:name": "...",
      "schema:url": "https://example.org/data/stations"
    }
  }]
  ```
- **Description:** Use schema.org `relatedLink` with a `LinkRole` value, and the link URL in a `target` EntryPoint object. These properties expect WebPage and Action as their domain, so the [schema.org validator](https://validator.schema.org/) will throw a warning (not an error). Related-resource links are useful for evaluation and use of data, but because of the wide variety of relationship possibilities they are difficult to use in general search scenarios. Use a soft-type implementation, with a link-relationship type using a `schema:DefinedTerm`, and a resolvable identifier for the relationship target.

## Funding
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:funding": [{
    "@type": "schema:MonetaryGrant",
    "schema:identifier": {
      "@type": "schema:PropertyValue",
      "schema:propertyID": "grant-id",
      "schema:value": "..."
    },
    "schema:name": "grant title",
    "schema:funder": {
      "@id": "https://ror.org/...",
      "@type": "schema:Organization",
      "schema:name": "org name"
    }
  }]
  ```
- **Description:** Use schema.org encoding and the [Science on Schema.org pattern](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#funding). Other organization properties can be included in the funder Organization.

## Policies
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:publishingPrinciples": [{
    "@type": "schema:CreativeWork",
    "schema:name": "...",
    "schema:url": "..."
  }, ...]
  ```
- **Description:** FDOF `digitalObjectMutability`, RDA `digitalObjectPolicy`, FDOF `PersistencyPolicy`. Policies related to maintenance, update, and expected time to live.

## Checksum
- **Cardinality:** 0..1
- **JSON:**
  ```json
  "schema:distribution": [{
    "@type": ["schema:DataDownload"],
    "spdx:checksum": {
      "@type": "spdx:Checksum",
      "spdx:algorithm": "SHA256",
      "spdx:checksumValue": "abc123..."
    },
    ...
  }, ...]
  ```
- **Description:** A string value calculated from the content of the resource representation, used to test if content has been modified. No schema.org property; follow DCAT v3 adoption of the [Software Package Data Exchange (SPDX)](https://spdx.org/rdf/terms/) property. The `spdx:Checksum` object has two properties: `algorithm` and `checksumValue`. The checksum is a property of each distribution / DataDownload.

## Provenance for discovery
Provenance for discovery is limited to documenting technology used in the creation of the dataset and documenting other datasets that were inputs to the content of the described resource. The cdifDiscovery profile specifies only that `prov:wasGeneratedBy` has a `prov:Activity` with `prov:used` items that are strings or `@id` references. Any additional structure under `prov:used` is optional and defined by extended profiles.

### *Provenance (instruments, software, etc.)*
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "prov:wasGeneratedBy": [{
    "@type": ["prov:Activity"],
    "prov:used": [
      "nerc:collection/L05/current/134",
      {"@id": "nerc:collection/B76/current/B7600031"}
    ]
  }]
  ```
- **Description:** Identify sensors, instruments, platforms, software, algorithms, etc. used in the creation of the described resource. The `prov:used` array accepts strings (URIs or labels) or object reference (`{"@id": "..."}`).

### *Provenance (input datasets)*
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "prov:wasDerivedFrom": [
    "http://doi.org/10.547/347848",
    {"@id": "http://doi.org/10.3578/h5ls"},
    {"@type": "schema:CreativeWork", "schema:name": "...", "schema:url": "..."}
  ]
  ```
- **Description:** Identify datasets that were inputs to the content of the described resource. Items can be strings (URIs), object reference (`{"@id": "..."}`), or CreativeWork objects with name and URL.




## Service-based distribution
An API builds on a basic communication protocol (e.g. HTTP) by defining functionality and formatting to enable providing the specific data a user requires. This might involve filtering, subsetting, or various transformations for e.g. schema mapping, aggregating or anonymizing data. The focus here is on Web APIs that provide data using a URL for the endpoint location (the server that implements the data access protocol), with parameters to specify the particular data requested. The query parameters might be appended to this base URL as part of the URL, or provided as a message with the request. The implementation is based on the schema.org Action patterns. A WebAPI distribution is included as an item in the `schema:distribution` array alongside DataDownload items.

Implementation of metadata to describe a service-based (API) distribution:

## Service type
- **Cardinality:** 1
- **JSON:**
```json
  "schema:distribution": [{
    "@type": ["schema:WebAPI"],
    "schema:serviceType": "{string or DefinedTerm}"
  }]
```
- **Description**: Specify the kind of service. Ideally this should be a resolvable identifier. Currently there is no widely adopted registry for serviceType identifiers. For interoperability, there must be an external arrangement between data providers and consumers on the strings that will be used to specify service types.
## Service description document
- **Cardinality**: 0..1
- **JSON**:`"schema:documentation": "{string or CreativeWork}"`
- **Description**: Document that provides a machine-actionable description of a service instance. Examples include OpenAPI documents, OGC Capabilities documents.
## Endpoint URL
- **Cardinality**: 1
- **JSON**:
```"schema:potentialAction": [{
  "@type": ["schema:Action"],
  "schema:target": {
    "@type": "schema:EntryPoint",
    "schema:urlTemplate": "..."
  }
}]
```
- **Description**: Web location to invoke service; if there are parameters on the URL, the URL template construct enables description of the parameters.
## Access constraints
- **Cardinality**: 1
- **JSON**:`"schema:termsOfService": "{string or CreativeWork}"`
- **Description**: Description of access privileges required to use the API, e.g. registration, licensing, payments.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/datatypes.md

# Common Data Types

Several JSON-LD encoding patterns recur across the CDIF profiles. They are defined once here and referenced from the individual profile pages. All property names use namespace prefixes declared in each document's `@context` (`schema:`, `skos:`, `dcterms:`, `cdi:`, `xsd:`, etc.).

(object-reference)=
## Object Reference

A reference to another node by its `@id`, used to link to an object defined elsewhere in the same document, in another CDIF document, or externally. An object reference carries no other properties — it is resolved by matching its `@id` to the full node definition.

- **JSON:** `{"@id": "uri for target"}`
- **Scope note:** An 'object reference' indicates that a property value is specified with a URI rather than an inline object. The `@id` value must be a resolvable identifier that yields a JSON object of the type the property expects. For some elements the target is an `@id` node defined elsewhere in the same document; otherwise it should be a resolvable HTTP URI for an external resource.

(languagetaggedvalue)=
## LanguageTaggedValue

An RDF literal with a language tag, serialized as a JSON-LD value object.

- **JSON:** `{"@value": "Natural Solid Material", "@language": "en"}`
- **Scope note:** `@value` is the text content; `@language` is a [BCP 47](https://www.rfc-editor.org/info/bcp47) language tag (e.g. `en`, `fr`, `de`, `sv`). Use an array of LanguageTaggedValue objects to provide a label or text in multiple languages.

(sec-definedterm)=
## DefinedTerm

A `schema:DefinedTerm` represents a concept drawn from a controlled vocabulary, providing a human-readable name together with a resolvable identifier and a link to the vocabulary that defines it.

- **JSON:**
  ```json
  {
    "@type": ["schema:DefinedTerm"],
    "schema:name": "{string}",
    "schema:identifier": "{URI}",
    "schema:inDefinedTermSet": "{URI}",
    "schema:termCode": "{string}"
  }
  ```
- **Scope note:** Use a DefinedTerm (rather than a plain string) whenever a value comes from a known vocabulary. `schema:name` is the label, `schema:identifier` the concept URI, `schema:inDefinedTermSet` the vocabulary URI, and `schema:termCode` an optional short code. A [skos:Concept](#sec-skosconcept) may be used instead where a fuller SKOS description is available.

(sec-xsddatatype)=
## xsdDataType

The XML Schema datatype that constrains the lexical form of a value, given as a CURIE in the `xsd:` namespace.

- **JSON:** `"xsd:double"` (e.g. `xsd:string`, `xsd:integer`, `xsd:double`, `xsd:date`, `xsd:dateTime`, `xsd:boolean`, `xsd:anyURI`)
- **Scope note:** Identifies the primitive datatype used to interpret values, drawn from the [XML Schema built-in datatypes](https://www.w3.org/TR/xmlschema11-2/#built-in-datatypes). Use where a variable or value domain needs an unambiguous machine-readable datatype.

(sec-propertyvalue-vm)=
## PropertyValue (variableMeasured)

The Discovery-profile shape for a `schema:variableMeasured` item: a `schema:PropertyValue` describing one variable in a dataset. The Data Description profile extends this base with additional CDIF properties.

- **JSON:**
  ```json
  "schema:variableMeasured": [{
    "@type": ["schema:PropertyValue"],
    "@id": "astm:var0011",
    "schema:propertyID": ["pato:PATO_0000025", "astm:prop/0405"],
    "schema:name": "hostMineral",
    "schema:description": "..."
  }]
  ```
- **Scope note:** Base properties available on every `variableMeasured` item: `@id`, `schema:name`, `schema:description`, `schema:alternateName`, `schema:propertyID` (URI(s) for the represented concept — the semantic linkage for the variable's meaning), `schema:measurementTechnique`, `schema:unitText`, `schema:unitCode`, `schema:minValue`, `schema:maxValue`, `schema:url`. Follows the [ESIP Science on Schema.org](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables) recommendation.

(sec-propertyvalue-id)=
## PropertyValue (identifier)

A `schema:PropertyValue` used to express a structured identifier when a plain resolvable URI does not make the identifier scheme or resolution process clear.

- **JSON:**
  ```json
  {
    "@type": ["schema:PropertyValue"],
    "schema:propertyID": "https://registry.identifiers.org/registry/doi",
    "schema:value": "10.5683/SP2/TTJNIU",
    "schema:url": "https://doi.org/10.5683/SP2/TTJNIU"
  }
  ```
- **Scope note:** The ESIP Science on Schema.org guidance recommends serializing identifiers as `schema:PropertyValue`. CDIF suggests using this approach only for identifiers whose URI does not make the authority clear or whose resolution process is not well known; otherwise a simple URI string is sufficient.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/dcat.md

# Data Catalog Vocabulary (DCAT) vocabulary

[DCAT](https://www.w3.org/TR/vocab-dcat-3/) is an RDF vocabulary designed to facilitate interoperability between data catalogs published on the Web. DCAT enables a publisher to describe datasets and data services in a catalog using a standard model and vocabulary that facilitates the consumption and aggregation of metadata from multiple catalogs.  The current DCAT version 3 has been developed by the [Dataset eXchange Working Group (DXWG)](https://www.w3.org/2017/dxwg/wiki/Main_Page) of the World Wide Web Consortium (W3C). DCAT has become very common in some areas: [DCAT-AP](https://semiceu.github.io/DCAT-AP/releases/3.0.0/) and [GeoDCAT](https://joinup.ec.europa.eu/collection/semic-support-centre/solution/geodcat-application-profile-data-portals-europe) have gained significant traction in Europe. [DCAT-US](https://doi-do.github.io/dcat-us/) promises to gain similar traction. 

The scope of [Schema.org](https://schema.org/) is much broader than DCAT, and includes any business activity on the Web. DCAT is designed for describing data and thus has some features that are specifically useful for CDIF’s purposes. There are several different mappings between Schema.org and DCAT available, and some may be more appropriate than others for any particular implementation. CDIF recommends the mapping from the W3C DXWG group. The mapping in the context of DCAT version 2 is at 
https://ec-jrc.github.io/dcat-ap-to-schema-org/ or https://www.w3.org/TR/vocab-dcat-2/#dcat-sdo 

https://w3c.github.io/dxwg/dcat/rdf/dcat-schema.ttl is a mapping between DCAT2 and SDO 3.4. axiomatized using the predicates rdfs:subClassOf, rdfs:subPropertyOf, owl:equivalentClass, owl:equivalentProperty, skos:closeMatch, and using the annotation properties sdo:domainIncludes and sdo:rangeIncludes to match [Schema.org](https://schema.org/) semantics. 

There is an update for the mapping in the [DCAT version 3 documentation](https://www.w3.org/TR/vocab-dcat-3/#dcat-sdo)

DCAT metadata is typically serialized using the [Turtle format](https://www.w3.org/TR/turtle/), so the implementation guideline here are based on that format.

# Implementation of metadata content items

The following table maps the metadata content items described in the [Metadata Content Requirements](./contentmodel.md) section to the RDF terms defined by the DCAT specification for use in metadata serialization. The \'Obl.\' column specifies the cardinality obligation for the property; \'1\' means one value required; 1..\* means at least one value is required; 0..\* means the property is optional and more that one value can be provided. 


|**CDIF content item**|**Obl.**|**DCAT v3 implementation**|**Scope note**|
|-----------|---|--------------|----------------------------------------------|
Metadata identifier|1|ex:record-001<br>  a dcat:CatalogRecord ;<br>  foaf:primaryTopic ex:dataset-001 ;|ex:record-001 in the implementation has type 'dcat:CatalogRecord', and is a graph node that contains information about the metadata record for the a resource indicated by the foaf:primaryTopic. The use of dcat:CatalogRecord is considered optional. It is used to capture provenance information about entries in a catalog explicitly.
Resource identifier|1|ex:dataset1URI a dcat:Resource; <br>  dcterms:identifier  "string literal";|The dcterm:identifier is the identifer for the thing in world that is the subject of the DCAT record. The DCAT record is a representation of that thing as a digital object, and the subject of the '\<uri\> a  dcat:Resource' triple typically identifies the same thing; that URI might dereference to GET a different representation for the thing in the world.  The subject of the \<uri\> a  dcat:Resource' triple is like the JSON-LD @id value, which identifies a graph node that can be interpreted either as the thing in the world the graph node is about, or the JSON-LD (or other RDF serialization) object that is the web representation of that thing. 
Title|1|a dcat:Resource;<br>    dcterms:title  "string literal"@lan;|A set of words that should uniquely identify the described resource for human use, in the scope of the metadata catalog containing this metadata record.  Titles should be language localized with @lan tags; only one distinct title per @lan tag is allowed.
Distribution|1|a dcat:Resource; <br>   dcat:landingPage  "literal string URL";|URL for a web location that provides information about the resource, generally expected to include information about how to get the resource.  In general, a resource should have only one landing page.
| | | a dcat:Dataset; <br>    dcat:distribution [<br>        a dcat:Distribution;<br>            dcat:downloadURL  "literal URL string" ];|URL for web location that will get a representation of the described resource. downloadURL is **required**. The Distribution object SHOULD include dcat:mediaType to specify the media type for the actual resource representation; if the distribution content is compressed or packaged, dcat:compressFormat or dcat:packageFormat SHOULD be specified as well. dcterm:conformsTo can be used to identify a specification that defines the full syntax and semantics for the resource content. Other properties in the dcat:Distribution object can be used to provide information about content size, rights, policies, etc. for the particular representation of the resource.
|| | a  dcat:Dataset;<br>    dcat:distribution [<br>       a dcat:Distribution;<br>       dcat:accessURL  "literal URL string"];|URL for a web location that provides information about how to get the resource.  The accessURL might be the same as the landing page, but different distributions might offer different web applications (with different accessURLs) for different access methods or communities. The target of the URL MUST be a web page that can be displayed in standard web browsers.
Rights|1..\*| |[DCAT uses several properties](https://www.w3.org/TR/vocab-dcat-3/#license-rights) to convey information about access or usage limitations: dcterms:accessRights, dcterms:license and dcterms:rights, which all apply to any dcat:Resource or dcat:Distribution. 'dcterms:license' is used to associate a resource with a statement that is explicitly declared as a 'license'. 'dcterms:accessRights' when the resource is associated with a statement denoting only access rights. 'dcterms:rights for other cases,   associating statements not concerning licensing conditions or access rights (e.g., copyright statements).  CDIF requires that at least one of these rights properties is populated, either at the dcat:Resource level, applying to all distributions, or with a rights property on each dcat:Distribution. 
| | | a dcat:Resource OR dcat:Distribution; <br>    dcterms:accessRights [ <br>&nbsp;&nbsp;	rdf:type dcterms:RightsStatement ;<br> &nbsp;&nbsp;	rdfs:comment "literal rights statement"@en];  <br>&nbsp;&nbsp; OR \<Rights statement URI\>;|A statement or link to a statement associated with a resource or a specific resource distribution, denoting access rights, applicable to any distribution of the resource. Access rights can also be expressed as code lists / taxonomies. Examples include the access rights code list [EUV-AR](https://publications.europa.eu/en/web/eu-vocabularies/at-dataset/-/resource/dataset/access-right) used in [DCAT-AP]( https://joinup.ec.europa.eu/solution/dcat-application-profile-data-portals-europe) and the [Eprints Access Rights Vocabulary Encoding Scheme](http://purl.org/eprint/accessRights/).
|| |a  dcat:Resource OR dcat:Distribution; <br>        dcterms:license [ <br>&nbsp;&nbsp;	rdf:type dcterms:LicenseDocument ;<br> &nbsp;&nbsp;	rdfs:comment "literal license statement or identifier"@en];  <br>&nbsp;&nbsp; OR \<License URI\>;|link to a statement associated with a resource that is explicitly declared as a 'license'. Can be applied at the dcat:Resource or dcat:Distribution level. For interoperability, it is recommended to use canonical IRIs of well-known licenses such as those defined by Creative Commons.  
| | |a dcat:Resource OR dcat:Distribution; <br>    dcterms:rights  [ <br>&nbsp;&nbsp;	rdf:type dcterms:RightsStatement ;<br> &nbsp;&nbsp;	rdfs:comment "literal rights statement"@en];  <br>&nbsp;&nbsp; OR \<Rights statement URI\>;| link to a statement associated with a resource for other types of rights statements, i.e. those that are not covered by dcterms:license and dcterms:accessRights, such as copyright statements. NOTE-- odrl:hasPolicy property is available at the dcat:Resource or dcat:Distribution level if a formal ORDL rules statement is available (see [example](https://www.w3.org/TR/vocab-dcat-3/#ex-odrl-policy) ).  
Metadata profile identifier|1|a dcat:CatalogRecord ;<br>      foaf:primaryTopic \<ex:dataset1URI\> ;<br>      dcterms:conformsTo \<specification uri\>;|The conformsTo property on the CatalogRecord specifies the metadata profile followed by the actual metadata record identified by foaf:primaryTopic. The dcat:CatalogRecord object is a separate node from the dcat metadata node whose subject is the described resource.
Metadata date|0..1|a dcat:CatalogRecord ;<br>  foaf:primaryTopic \<ex:dataset1URI\> ;<br>  dcterms:modified "date string"^^xsd:dateTime;|Use ISO8601 format. The most recent update date for the metadata content is specified in the modififed property on the CatalogRecord linked to the metadata record identified by foaf:primaryTopic.. Harvesters use this to determine if they have already harvested and processed this record.
Metadata contact|0..1|a dcat:CatalogRecord ;<br>  foaf:primaryTopic \<ex:dataset1URI\> ;<br>  dcat:contactPoint [ <br>  &nbsp;&nbsp; a  vcard:Kind;<br> &nbsp;&nbsp;   v:hasEmail \<mailto:name@email.org\> ;<br>&nbsp;&nbsp;   v:fn "full Name"; <br> &nbsp;&nbsp;  rdfs:label "Full Name"];|Not in DCAT CatalogRecord. Add a dcat:contactPoint property on CatalogRecord, based on open-world RDF.  The vcard:Kind must be an individual or organization. Including rdfs:label is optional, but recommended for interoperability.
Resource type|1..\*|rdf:type {DCAT class};<br>   dcterms:type  \<uri for resource type\>;|The nature or genre of the resource. The rdf:type Must be a DCAT class; currently Resource, Dataset, DatasetSeries, and DataCatalog are applicable for CDIF.  A more sepecific type can be assigned using dcterms:type; the value SHOULD be taken from a well governed and broadly recognised controlled vocabulary. Use of Schema.org types will promote interoperability. Multiple types can be specified.
Description|0..1|a dcat:Resource;<br>    dcterms:description "free text description of resource";|Free text, with as much detail as is feasible
Originators|0..\*|a dcat:Resource;<br>    dcterms:creator [ <br> &nbsp;&nbsp; a  foaf:Agent;<br>   &nbsp;&nbsp; foaf:name "name of agent";<br> foaf:mbox \<mailto:email\@email.org\>; <br> sdo:identifier \<agent URI \>;  ]|The value is foaf:Agent, or foaf:Person or foaf:Organization (subclasses of foaf:Agent. foaf:name is required. The foaf spec provides properties for a name and e-mail address. DCAT examples use the [adms:identifier](https://semiceu.github.io/ADMS/releases/2.00/), but since CDIF used schema.org, the schema.org identifier property is recommended. Value should be a PID. Use ORCID to identify person or ROR to identify organization if possible.  
Publication Date|0..1|a dcat:Resource; <br>   dcterms:issued "date string"^^xsd:dateTime;|Date on which the resource was made publicly accessible. Use ISO 8601 format.
Modification Date|1|a dcat:Resource; <br>   dcterms:modified  "date string"^^xsd:dateTime;|Date of most recent update to resource content. If Publication date is not provided, defaults to the Modification Date. Use ISO 8601 format.
GeographicExtent (named place)|0..\*|a dcat:Dataset; <br>   dcterms:spatial  "string literal place name"  <br>OR<br>a dcat:Dataset; <br>    dcterms:spatial \<location URI\> "|To specify location with place name as a string or a URI (or IRI) from a gazetteer.
GeographicExtent (bounding box)|0..1|a dcat:Dataset; <br>  dcterms:spatial [<br>    a dcterms:Location ;<br>    dcat:bbox ""POLYGON((<br>      103.05 47.9 , 107.2  47.9 ,<br>      107.2  53.5 , 103.0 53.5 ,<br>      103.0 47.9     ))""^^geosparql:wktLiteral ;<br>  ] ;"|The range of dcat:bbox is rdfs:Literal. CDIF requires that the box geometry is encoded as a WKT literal ([geosparql:wktLiteral](https://docs.ogc.org/is/22-047r1/22-047r1.html), using WGS84. Coordinate pairs are {longitude latitude} decimal number pairs, with a space between coordinates. Commas separate coordinate pairs. The first and last coordinate must be the same to close the box.  Coordinates are listed in a counterclockwise order around the box perimeter. CDIF recommends including only one bounding box; behavior of harvesting clients when multiple geometries are specified is unpredictable.  See [ESIP SOSO](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes) for more details.
GeographicExtent (point location)|0..1|a dcat:Dataset; <br>  dcterms:spatial [<br>    a dcterms:Location ;<br>    locn:geometry  "POINT (103.05 47.9)"^^geosparql:wktLiteral ;<br>  ];"|For a point location specification of the spatial extent of resource content. Note use of locn:geometry from the [Location Vocabulary](https://semiceu.github.io/Core-Location-Vocabulary/releases/2.1.0/#Resource.geometry). Recommend including only one point; behavior of harvesting clients when multiple geometries are specified is unpredictable.  Note DCAT reports point locations only as centroids; CDIF is more general-- point locations might be centroids or any point within or near (in the case of intentionally spoofed locations) the resource location.
GeographicExtent (other serialization)|0..\*|a dcat:Dataset;<br>  dcterms:spatial [<br>    a dcterms:Location ;<br>    locn:geometry  {see [Location Vocabulary](https://semiceu.github.io/Core-Location-Vocabulary/releases/2.1.0/#Resource.geometry)}  ]; |Optional geographic extent using other serialization for location. Other geometry schemes might be specified in a specific domain profile, e.g. for atmospheric, subsurface data, or local coordinate systems. These will likely not be interoperable across domains.
Variable (PopertyValue) |0..\*|a dcat:Dataset; <br>  sdo:variableMeasured [ <br>&nbsp;&nbsp; a sdo:PropertyValue; <br>&nbsp;&nbsp; propertyID \<pato:PATO_0000025\>, \<astm:prop/0405\>; <br> &nbsp;&nbsp;sdo:name "hostMineral";<br> &nbsp;&nbsp;sdo:description "…."; ….]"|Follow [ESIPfed Science on Schema.org recommendation](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables), see also discussion for representing more complex data structures in [ESIPfed Experimental](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Experimental.md#AdvancedVariableValueType) and the [Data Integration module of CDIF](https://cross-domain-interoperability-framework.github.io/cdifbook/data_integration/ddidescriptiondatastructure.html). Variable must have a name and description, should have a propertyID with URI for the represented concept. The URI in the propertyID provides the semantic linkage for meaning of the variable. dcat does not have properties to specify variables/properties quantified in a cataloged resource.
Variable (Statistical Variable) |0..\*|a dcat:Dataset; <br>  sdo:variableMeasured [ <br>&nbsp;&nbsp; a sdo:StatisticalVariable; <br>&nbsp;&nbsp; sdo:measuredProperty <br> a sdo:Property; \ <br> sdo:identifier \<https://properties.org/id/305978\>\; sdo:name "Average age";| Statistical variable offers properties useful for describing social science statistical variables like populationType and statType. Use of StatisticalVariable is preferred for variables with values calculated from some aggregation process. |
Keyword|0..\*|a dcat:Resource; <br>  dcat:keyword "string literal";|Implement with text for tags, free text words useful for indexing the resource.
|| | a dcat:Resource; <br>  dcat:theme \<uri\>  <br>OR  <br>a dcat:Resource; <br>  dcat:theme [ <br>    \<concept URI\>  a skos:Concept;<br>    skos:prefLabel "term"@languageCode]|A main category of the resource. A resource can have multiple themes.  Expectation is that the set of themes used to categorize  resources are organized in a structured vocabulary describing all the categories and their relations in the catalog, e.g.  skos:ConceptScheme, skos:Collection, owl:Ontology. Note dcat:theme in dcat OWL is an object property, the type of the object is not specified. In the example to the left the theme object is typed 'skos:Concept', but could be other type.
Temporal coverage|0..1|a dcat:Dataset; <br>  dcterms:temporal<br>   [ a dcterms:PeriodOfTime ;<br>      dcat:startDate<br>&nbsp; "2016-03-04"^^xsd:date ;<br> dcat:endDate<br>&nbsp;  "2018-08-05"^^xsd:date ;<br>   ];|Calendar data or clock time interval.  rdfs:Literal encoded using the relevant ISO 8601 Date and Time compliant string [DATETIME](https://www.w3.org/TR/NOTE-datetime) and typed using the appropriate XML Schema datatype [XMLSCHEMA11-2](https://www.w3.org/TR/xmlschema11-2/), i.e. xsd:gYear, xsd:gYearMonth, xsd:date, or xsd:dateTime.  The range of dcterms:temporal is expected to be PeriodOfTime; to specify a time instant the start and end should be the same.  [tbd: add note on other temporal options offered by DCAT]
|| |a dcat:Dataset; <br>  dcterms:temporal [ <br>    a dcterms:PeriodOfTime ,<br>&nbsp;&nbsp; time:ProperInterval ;<br>      time:intervalStartedBy<br>&nbsp;&nbsp; \<isc:LowerDevonian\>;<br>      time:intervalFinishedBy<br> &nbsp;&nbsp;\<isc:LowerPermian\>];|Time ordinal era interval, use owl:time namespace, time: http://www.w3.org/2006/time#. This example uses International chronostratigraphic chart [ISC](https://stratigraphy.org/chart). See https://perio.do/en/ for identifiers for many other named time intervals.
|| | a dcat:Dataset; <br>  dcterms:temporal [<br>   a dcterms:PeriodOfTime , <br>&nbsp;&nbsp; &nbsp; time:ProperInterval ;<br>    time:hasBeginning [   a time:Instant ;<br>      time:inTimePosition [  a time:TimePosition ;<br>             time:hasTRS \<gsmla:ma\> ;<br>             time:numericPosition "541.0"^^xsd:decimal <br>   ]  ] ;<br>    time:hasEnd [ a time:Instant ;<br>      time:inTimePosition [   a time:TimePosition ;<br>          time:hasTRS \<gsmla:ma\> ;<br>   time:numericPosition "251.9"^^xsd:decimal  <br>]   ] ]; |Temporal coverage for a geologic dataset, with interval bounds specified with numericPositions in millions of years before present.  Namespace abbreviation: gsmla: http://resource.geosciml.org/classifier/cgi/geologicage/
Related agent - point of contact| |a dcat:Resource; <br>&nbsp; dcat:contactPoint [<br>&nbsp; &nbsp;  a  vcard:Kind ;<br>&nbsp;&nbsp;	vcard:hasEmail \<mailto:email@email.org\> ;<br>&nbsp;&nbsp; vcard:fn "Full Name" .] ;| DCAT defines a  property on any dcat:Resource for the 'point of contact' role. Use Individual or Organization subclass of vcard:Kind.
Related agent - publisher| |a dcat:Resource; <br>&nbsp; dcat:publisher [<br>&nbsp; &nbsp;  a  foaf:Agent ;<br>&nbsp;&nbsp;	foaf:mbox \<mailto:email@email.org\> ;<br>&nbsp;&nbsp; foaf:name "Full Name" .] ;| DCAT defines a  property on any dcat:Resource for the 'publisher' role. Use Person or Organization subclass of foaf:Agent.
Related agent with role| |a dcat:Resource, prov:Entity; <br>&nbsp; prov:qualifiedAttribution [<br>&nbsp; &nbsp;     a prov:Attribution ;<br>  &nbsp; &nbsp;   prov:agent \<agent URI\> ;<br>    &nbsp; &nbsp; dcat:hadRole \<role URI\><br>  ];|To assign roles to contributors like editor, maintainer, compiler, rightsOwner, etc..  Note [PROV-O](https://www.w3.org/TR/prov-o/) roles relate to activities, not entities. Therefore, DCAT defines a new property dcat:hadRole  to attach a role to the association-class prov:Attribution between and entity and an agent. [MARC relators](https://id.loc.gov/vocabulary/relators.html) provide many relationships between resources and agents.
Related agent - distributor |0..\*|a dcat:Resource, prov:Entity; <br>  prov:qualifiedAttribution [<br>&nbsp;&nbsp;   a prov:Attribution ;<br> &nbsp;&nbsp;   prov:agent \<agent URI\> ;<br>&nbsp;&nbsp;  dcat:hadRole \<distributor role URI\><br>  ];|To assign an agent to a distributor role.  Note [PROV-O](https://www.w3.org/TR/prov-o/) roles relate to activities, not entities. Therefore, DCAT defines a new property dcat:hadRole  to attach a role to the association-class prov:Attribution between and entity and an agent.  Note that in DCAT prov:qualifiedAttribution can only be used with dcat:Resource or subclass of dcat:resource, not with individual distributions. CDIF recommendation for the role uri is 'http://id.loc.gov/vocabulary/relators/dst'. 
| | | a dcat:Dataset; <br> &nbsp;dcat:distribution [<br>&nbsp;&nbsp;&nbsp;a dcat:Distribution;<br>&nbsp;&nbsp;&nbsp;sdo:provider [<br>&nbsp;&nbsp;&nbsp;&nbsp;a sdo:Person OR sdo:Organization] <br>];|If there are multiple distributions with different providers, each distribution can have a separate provider. dcat:Distribution does not have pointOfContact or prov:qualifiedAttribution. 
Related resources|0..\*|a dcat:Resource;<br>   \<dcterms:relation or subProperty\> <br> &nbsp; &nbsp; \<target resource URI\>|dcterms:relation is used if the nature of the relationship between a cataloged resource and related resources is not known. More specific sub-properties of relation (dcterms:hasPart, dcterms:isPartOf, dcterms:conformsTo, dcterms:isFormatOf, dcterms:hasFormat, dcterms:isVersionOf, dcterms:hasVersion (and its sub-property dcat:hasVersion ), dcterms:replaces, dcterms:isReplacedBy, dcterms:references, dcterms:isReferencedBy, dcterms:requires, dcterms:isRequiredBy)  SHOULD be used if the nature of the relationship of the link is known.  These dcterms relation types will have to be mapped to linkRelationship values in schema.org to map between the schema. Note that the target of the relation should be a resolvable URI.
| |0..\*|a dcat:Resource;<br>   dcat:qualifiedRelation [<br>    a dcat:Relationship ;<br>    dcterms:relation \<target resource URI\> ;<br>    dcat:hadRole \<relationship type URI\><br>  ]; |Representation of relationship that are not hard typed by dcterms or dcat, e.g. alternate, canonical, original, preview, stereo-mate, working-copy-of. Some of these roles are enumerated in the DS_AssociationTypeCodes values from [ISO-19115-1](https://standards.iso.org/iso/19115/resources/Codelists/gml/DS_AssociationTypeCode.xml), the IANA Registry of Link Relations [IANA-RELATIONS](https://www.iana.org/assignments/link-relations/), in the [DataCite](https://schema.datacite.org/meta/kernel-4.5/include/datacite-relationType-v4.xsd) metadata schema, and included within the [MARC relationships](https://id.loc.gov/vocabulary/relationship.html).  Ideally a resolvable URI is available for the relationship role.
Funding|0..\*|a dcat:Resource, prov:Entity;<br>&nbsp; prov:qualifiedAttribution [<br>&nbsp; &nbsp;  a prov:Attribution ;<br> &nbsp; &nbsp;  prov:agent \<agent URI\> ;<br> &nbsp; &nbsp;  dcat:hadRole \<role URI\><br>];|To assign roles to a funding instrument.  Note [PROV-O](https://www.w3.org/TR/prov-o/) roles relate to activities, not entities. Therefore, DCAT defines a new property dcat:hadRole  to attach a role to the association-class prov:Attribution between and entity and an agent.  In this case the prov:agent should be a funding instrument (e.g. identified grant) under the auspices of a funding agency, and role should indicate that the agent is the provider of funding to create the resource
Policies|0..\*|a dcat:Resource OR dcat:Distribution<br>  odrl:hasPolicy [a odrl:Policy; ….];|DCAT provides a property odrl:hasPolich that has an ordl:Policy object as its targert, for both Resources, and individual distributions.  More work is necessay to determ how policies like    FDOF digitalObjectMutability, RDA digitalObjectPolicy, FDOF PersistencyPolicy can (or should) be expressed as ODRL policies and if there's a better implemention of these.  <br>An ODRL Policy MUST have one uid property value to identify the Policy, AND at least one permission, prohibition, or obligation property values of type Rule. (See the [ODRL model](https://www.w3.org/TR/odrl-model) Permission, Prohibition, and Obligation sections for more details.)
Checksum|0..1|a dcat:Distribution;<br>   spdx:checksum [<br>     a spdx:Checksum;<br>     spdx:algorithm \<algorithm URI\>;<br>     spdx:checksumValue   "nnnn"^^xsd:hexBinary ];|A string value calculated from the content of the resource representation, used to test if content has been modified. Use Software Package Data Exchange (SPDX) property; The [spdx Checksum](https://spdx.org/rdf/spdx-terms-v2.3/#d4e2091) object has two properties: algorithm and checksumValue. The checksum is a property of each distribution/Distribution
|Provenance (instruments, software etc.)|0..*|prov:wasGeneratedBy <br> a prov:Activity;<br>  prov:used <br>      \<nerc:collection/L05/current/134\>,   \<nerc:collection/B76/current/B7600031\> \] } |Identify sensors, instruments, platforms, software, algorithms etc. used in the creation of the described resource |
| Provenance (input datasets)|0..* |prov:wasDerivedFrom <br> \<http://doi.org/10.547/347848\>,        \<http://doi.org/10.3578/h5ls\>, \<http://doi.org/10.547/93578\> |Identify datasets used  in the creation of the described resource |
|Quality measure |0..* |"dqv:hasQualityMeasurement <br>    a dqv:QualityMeasurement; <br> &emsp; dqv:isMeasurementOf  &emsp;&emsp;&nbsp;&nbsp;\<nerc:collection/L27/current/ARGO_QC\>; &emsp;&emsp;dqv:value  "good";      |Quality assesment or measument conducted using procedure or protocol specified by the dqv:isMeasurementOf property, with result value specified in the dqv:value property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment. |

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/discovery.md

# Discovery Profile

Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/cdifDiscoveryStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/CDIFDiscoveryImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/discoveryRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/cdifDiscovery-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDiscovery/index.html)

The Discovery profile defines properties to document the spatial or temporal extent of the resource content or subject, and to document variables that are specified in a structured dataset. These properties are not included in core based on the observation that the information is not necessarily applicable to any kind of resource. 

See also [graphical presentation of Discovery Profile](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDiscovery/index.html)

Artefacts for the Discovery profile are in this [Github repository](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/tree/reviewRevision202606) (TBD--update link to release tag)

## Core elements
See [Core](core.md)

## Discovery metadata requirements
- **Geographic Extent** - (0..many)  Required if resource has a geographic extent for its subject, either a named location, bounding rectangle, linear trace, or point. To support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 84 datum. There are various other systems for describing location (see [Space](../universals/univgeography.md) ); these can be provided as alternate location descriptions, recognizing that they might be meaningful to some metadata harvesting agents. Some resources might not be usefully described by a WGS 84 extent, in which case indicate nil:notapplicable; this would include extraterrestrial resources, but named location can still be provided.
  - *Bounding Rectangle*: North Bounding Latitude, South Bounding Latitude, East Bounding Longitude, West Bounding Longitude. The minimum rectangle that completely contains the coverage extent for the resource content. Coordinate order and syntax are determined by the serialisation profile.
  - *Linear trace*: a linear trace e.g. of a ship's track, aircraft flight path, or surface traverse, represented as a series of points. Coordinate order and syntax are determined by the serialisation profile.
  - *Point*: Latitude, Longitude. A centroid point for the coverage extent of the resource, or the location of the resource content if a point location is appropriate. Coordinate order and syntax are determined by the serialisation profile.
  - *Named location*: Place name referenced to some gazetteer. Use scoped name pattern {label, authority, optional identifier}.
- **Temporal Coverage** (0..1 entry) Required if resource content is specific to some time interval. The time interval represented by or the subject of the described resource. This could be the time interval when data were collected, or an archaeological or geological time interval that is the subject of the resource. Need to account for clock time, calendar time (Gregorian, Julian, Hebrew, Islamic, Chinese, Mayan...), cyclical time (summer, first quarter, mating season, new moon, pay day) and for named time ordinal eras (Jurassic, Younger Dryas, Early Minoan I, Late Stone Age). See [OWL Time](https://www.w3.org/TR/owl-time/).
- **Variable** (0 to many entries): Required for datasets. The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be, ideally, qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text. Variable metadata should include as much content as needed for users to understand the type of the variable (e.g. measured, statistically derived, or simulated), its units, and any relevant reference systems for its values (see [Universals](../universals/univintro.md) ). Details of data structure and schema more closely related to interoperability, data integration, and usage than to data discovery are discussed in the [Data Description](../data_description/datadescriptionprofile.md) profile.
- **Measurement technique** (0..many) identifiers or names for measurement method used to acquire data.
- **Quality** (0..many) Provide statements about the quality of information in the described resource,  information about quality policies or certificates that apply to the resource, and results of quality measures with information about the measurement protocol/procedure used. In all cases the focus should be on information useful for initial assessment by potential users.


## Implementation of Discovery Extensions
Instance of the Discovery profile must conform to the requirements of the [core profile](core.md). The discovery profile adds these additional properties on the base Dataset element:

## Metadata profile identifier
- **Cardinality:** 1..*
- **JSON:**
  ```json
  "schema:subjectOf" / "dcterms:conformsTo": [
    {"@id": "https://w3id.org/cdif/discovery/1.1/"}
  ]
  ```
- **Description:** Note that the CDIF conformance class URIs are registered such that the base URI (e.g. https://w3id.org/cdif/discovery/1.1/) resolves to this implementation guidance page; add /schema and the uri will resolve to the JSON schema for validating instance documents using that profile; add /shacl and the shacl rules, encoded in turtle format, will be returned.

## Variables in the data
The metadata about a dataset should include a list of variables that the dataset contains. Variable metadata should minimally specify the name of the variable as it appears in the dataset. That name should be qualified by a controlled vocabulary or other semantic resource (e.g. represented by a resolvable URI), or minimally some descriptive text.

### Variable (PropertyValue)
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:variableMeasured": [{
    "@type": ["schema:PropertyValue"],
    "@id": "astm:var0011",
    "schema:propertyID": [
      "pato:PATO_0000025",
      "astm:prop/0405"
    ],
    "schema:name": "hostMineral",
    "schema:description": "..."
  }, ...]
  ```
- **Description:** Follow the [ESIP Science on Schema.org recommendation](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#variables); see also discussion for representing more complex data structures in [ESIP Experimental](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Experimental.md#AdvancedVariableValueType) and the [Data Description module of CDIF](https://cross-domain-interoperability-framework.github.io/cdifbook/data-description/datadescriptionforintegration/). Variable must have a name and description, should have a `propertyID` with URI for the represented concept. The URI in the `propertyID` provides the semantic linkage for the meaning of the variable.

### Variable (StatisticalVariable)
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "schema:variableMeasured": [{
    "@type": ["schema:StatisticalVariable"],
    "@id": "astm:var0011",
    "schema:measuredProperty": {
      "@type": "schema:Property",
      "schema:identifier": "astm:id/305978",
      "schema:name": "Average age"
    }
  }]
  ```
- **Description:** `StatisticalVariable` offers properties useful for describing social-science statistical variables like `populationType` and `statType`. Use of `StatisticalVariable` is preferred for variables with values calculated from some aggregation process.

### Temporal coverage
Temporal coverage is encoded as an array. It can be expressed in several ways: a calendar/clock dateTime or date-time interval using ISO 8601 serialization, a named time-ordinal era, an interval bounded by time-ordinal eras, or with a numeric coordinate in a temporal reference system.
- **Cardinality:** 0..*
### *Calendar date / clock time instant*
  - **JSON:**  `"schema:temporalCoverage": ["2018-01-22"]`
  - **Description:** Calendar date or clock time instant using ISO 8601 encoding.
### *Calendar date / clock time interval*
  - **JSON:**`"schema:temporalCoverage": ["2012-09-20/2016-01-22"]`
  - **Description:** Calendar date or clock time interval using ISO 8601 encoding.
### *Time ordinal era interval*
  - **JSON:**
    ```json
    "schema:temporalCoverage": [{
      "@type": "time:ProperInterval",
      "time:intervalStartedBy": "isc:LowerDevonian",
      "time:intervalFinishedBy": "isc:LowerPermian"
    }]
    ```
   - **Description:** Time-ordinal era interval, using the `owl:time` namespace (`time: http://www.w3.org/2006/time#`). This example uses the [International Chronostratigraphic Chart (isc)](http://resource.geosciml.org/classifier/ics/ischart/). See [PeriodO](https://perio.do/en/) for identifiers for many other named time intervals.
### *Geologic age interval (abbreviated form)*
  - **JSON:**`"schema:temporalCoverage": [{"time:ProperInterval-345/298 Ma"}]`
  - **Description:** For time intervals specified using geologic ages, in Ka, Ma, or Ga. The text string is an abbreviated `owl:time` interval (proposal, under discussion).
  
## Geographic extent
Required if the resource has a geographic extent for its subject — a bounding rectangle, line, or point. To support cross-domain searches based on geospatial location, location coordinates must be given in decimal degrees using the WGS 84 datum. Other systems for describing location can be provided as alternate descriptions, recognizing that they may not be meaningful to some metadata harvesting agents. Spatial coverage is encoded as an array.

### *Named place*
- **Cardinality:** 0..*
- **JSON:**
```json
  "schema:spatialCoverage": [{
    "@type": "schema:Place",
    "schema:name": {string} or {schema:DefinedTerm}
  }]
```
- **Description:** To specify location with place names. If the names are from a gazetteer, use the `schema:DefinedTerm` to provide a name, identifier, and `inDefinedTermSet` to fully document the concept.

### *Bounding box*
- **Cardinality:** 0..1
- **JSON:**
  ```json
  "schema:spatialCoverage": [{
    "@type": "schema:Place",
    "schema:geo": {
      "@type": "schema:GeoShape",
      "schema:box": "39.3280 120.1633 40.445 123.7878"
    }
  }]
  ```
- **Description:** For bounding-box specification of the spatial extent of resource content. See [ESIP SOSO for details](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/Dataset.md#bounding-boxes). Recommend including only one bounding box; behavior of harvesting clients when multiple geometries are specified is unpredictable.

### *Curvilinear trace*
- **Cardinality:** 0..1
- **JSON:**
  ```json
  "schema:spatialCoverage": [{
    "@type": "schema:Place",
    "schema:geo": {
      "@type": "schema:GeoShape",
      "schema:line": "39.33 120.77 40.44 123.96 41.00 121.34"
    }
  }]
  ```
- **Description:** For resources related to a linear trace like a ship track or airplane flight line.

### *Point location*
- **Cardinality:** 0..1
- **JSON:**
  ```json
  "schema:spatialCoverage": [{
    "@type": "schema:Place",
    "schema:geo": {
      "@type": "schema:GeoCoordinates",
      "schema:latitude": 39.3280,
      "schema:longitude": 120.1633
    }
  }]
  ```
- **Description:** For a point-location specification of the spatial extent of resource content. Recommend including only one point; behavior of harvesting clients when multiple geometries are specified is unpredictable.

### *Other serialization*
- **Cardinality:** 0..*
- **JSON:**
  ```json
  "geosparql:hasGeometry": {
    "@type": "sf:Point",
    "geosparql:asWKT": {
      "@type": "geosparql:wktLiteral",
      "@value": "POINT(-76 -18)"
    },
    "geosparql:crs": {"@id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"}
  }
  ```
- **Description:** Optional geographic extent using other more interoperable geometries. GeoSPARQL is recommended; see [Ocean InfoHub](https://book.oceaninfohub.org/thematics/spatial/README.html#simple-geosparql-wkt). Other geometry schemes might be specified in a specific domain profile, e.g. for atmospheric, subsurface data, or local coordinate systems.

## Quality information for discovery
A text statement documenting quality of the resource should be included in `schema:description`. If there are quality policies or certificates that apply, these should be specified in `schema:publishingPrinciples`. Quality measurements or assessment protocols that have an output result specific to this resource can be specified using `dqv:hasQualityMeasurement`.

- **Cardinality:** 0..*
- **JSON:**
  ```json
  "dqv:hasQualityMeasurement": [{
    "@type": "dqv:QualityMeasurement",
    "dqv:isMeasurementOf": "nerc:collection/L27/current/ARGO_QC",
    "dqv:value": "good"
  }, {
    "@type": "dqv:QualityMeasurement",
    "dqv:isMeasurementOf": "imf:dsbb/2003/eng/dqaf.htm",
    "dqv:value": "http://linkToASpecificQualityReport"
  }]
  ```
- **Description:** Quality assessment or measurement conducted using the procedure or protocol specified by the `dqv:isMeasurementOf` property, with the result value specified in the `dqv:value` property. The result might be numeric, a categorical term, or a link to a document describing the quality assessment.

## Measurement technique
- **Cardinality:** 0..*
- **JSON:** string or 
  ```
  "schema:measurementTechnique": [
    {
      "@type": ["schema:DefinedTerm"],
      "schema:name": "{string}",
      "schema:identifier": "{URI}",
      "schema:inDefinedTermSet": "{URI}",
      "schema:termCode": "{string}"
    }
  ],
  ```
- **Description:** A string or schema:DefinedTerm that specifies how the data were acquired.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/distributionapis.md

#  Queryable Distribution Interfaces (API)

Many resources are accessed using interfaces that allow customization of the resource representation and content that are delivered to a user. These interfaces are referred to as an API or 'Application Programming Interface', which is a specification of how to interact with a machine agent. Such a specification typically requires a communication protocol, description of the functions offered, and description of the content of messages transmitted between a client and the agent offering the interface. The focus of CDIF discovery is on communication protocols that use the internet and Hypertext Transfer Protocol (HTTP), which is the technology that underlies the World Wide Web. In this case the communication protocol can simply be specified as HTTP (or HTTPS). Various other protocols exist and new ones will be invented, these are out of scope for this recommendation.

Messages from a client to a service provider include, for example, requests to invoke some operation, requests to get content, and messages requesting information or providing information as part of a workflow (e.g. authentication, job status, inputs to configure processes). Messages from the service provider to the client include, for example, information about the service capabilities, status responses to requests (success, error..., in progress), or requested content or process results. The content of these messages uses a specific serialisation scheme to transmit information electronically, a syntax to make the content usable for machines, and some information model for semantic interoperability between the service provider and client. 

An API is defined by a specification (the instructions for how it works), implemented by some software, deployed on a server accessible to target clients, and accessed through an addressable endpoint using some communication protocol. The content offered using the API is not necessarily part of the API definition, but an API might be specific to a particular kind of content (e.g. photographs, digital maps, time-series data, tabular data, weather data, sound recordings). In general the particular content offered is specific to a service endpoint.

## Matching Data and Applications
In order to link data and applications, metadata for the data and for the application software must have sufficient information about the distribution protocol and format to determine whether an application can work with an offered distribution. The pattern is similar to that used by desktop computers to match files with applications, but more granular categorization of the distribution encoding format and information model is necessary to match data to applications offering functionality specific to that data.

From the software (data user) side of the connection, several factors come into play. The software might execute on an operating system like Linux, Windows, iOS, or Android, referred to here as 'standalone environment', or an application might execute in an online environment mediated by a Web browser application, referred to here as a 'browser environment'. In the standalone environment, an application has access to a local file system and various communication protocols and interfaces supported by the hosting operating system. We assume these include access to online resources using the internet. An internet-connected standalone application might implement a search function to find resources on the internet that work with the application.

In the browser environment, an application might run on a remote server and simply use the client browser as the user interface; at the other end of the spectrum, the server might download application code to the browser and the application runs in a browser container on the client side. In either case, the application execution would be started by an HTTP request to some Web location, and the HTTP protocol provides various mechanisms with the request that can be used to pass information specifying the target data for the application processing.

Search applications running in a Web browser will typically not be able to invoke an application to run outside of the browser's 'sandbox' for security reasons. In such cases, search results can list applications that will work with a particular dataset, and provide links to Web pages for additional information about how to install the application (if the user does not already have it installed), but the user will have to start that application and access the discovered data manually.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/mapping.md

# Metadata Mappings

This section contains some useful mappings between metadata schemes which may be useful for CDIF implementers. These include the mappings from CDIF to Persisitent Identifier (PID) Kernel attributes as defined by the RDA, and a descriptiob of how CDIF maps onto Signposting as a mechanism for Web navigation of FAIR resources.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/pidkernel.md

# Mapping from CDIF Metadata to RDA PID Kernel Attributes

In the Fair Digital Object Framework (FDOF) specifies that a Digital Object idnetifier (PID) can be resolved to obtain a PID kernel record. For the content of the PID kernel record we are following the RDA Recommendation on PID Kernel Information ([Weigel et al, 2019](https://www.rd-alliance.org/system/files/RDA%20Recommendation%20on%20PID%20Kernel%20Information_final.pdf) ). The implementation approach for supplying PID Kernel information records (See sections 3.1 and 3.2 in https://fairdigitalobjectframework.org/) associated with digital object identifiers is an architecture decision, not specified in this version of the CDIF framework. However, the information necessary to produce such metadata to implement the FDOF conventions is included in the CDIF metadata implementation, except for embedding of thumbnails or other data objects directly in the metadata digital object.


| **FDO field** | **CDIF schema.org** | **Scope Notes** |
| --- | --- | --- |
| <font size="3">FDO Creator</font> | "creator" : [{Person or Organization}, ...] | Agent responsible for creating the FDO (and implicitly issuing the FDO PID) [NOTE-- creator of content and identifier registration are not necessarily the same agent] |
| FDO Responsible Organisation (Resource) | "provider":{Person or Organization} | note that this can be another organisation than the PID issuer. If the agent is an organization, the value is taken from the ROR registry value domain (or other with namespace id). Implement as responsible part with an Agent (name, ID, contactInformation)  |
| RDA checksum | "spdx:checksum": | Checksum of object contents. Checksum format is determined via the attribute type referenced in a Kernel Information record. Called etag in [PubCom-PR-PIDProfileAttributes-2.0](https://docs.google.com/document/d/1QVUR6vlp6s6LxZndMslym9pmM90rFUR6__q3cuXSQf8/edit#heading=h.z337ya). The algorithm for checksum calculation should be defined in the definition of the object type, or described in the resource description in this metadata. spdx value is an object with 'algorthm' and 'checksumValue'. |
| FDOF digitalObject-Mutability | "publishingPrinciples": | This attribute indicates whether the included bit-sequence is mutable or immutable, and policies for when new version is created when some bits are changed.  Principles apply at the DigitalObject/Distribution level.|
| FDOF Persistency-Policy | "publishingPrinciples": | this attribute indicates what the intention of its creator is with respect to its life-time/maintenance; the value domain is a vocabulary like: {UNKNOWN, NONE, Years , or [EarthCube ELT](http://cor.esipfed.org/ont/earthcube/ELT) } (note: seems only partly covered by RDA digitalObjectPolicy.   |
| RDA digitalObject-Policy | "publishingPrinciples": | Pointer to a policy object that documents changes to the object or its Kernel Information record, including object access and modification policies. A caller should be able to determine the expected future changes to the object from the policy, which are based on managed processes the object owner maintains. |
| FDOF Responsible-Organisation (Technical Management) | "contributor": {"@type": "Role",<br> "roleName": "maintainer",<br>"contributor": {"@type": "Organization",<br>&emsp; "@id": {personID},<br>&emsp;"name": {personName},<br>*..other possible properties omitted* } } | after creation, the same or another organisation will be responsible for further management of the FDO. The Responsible Organisation equals the FDO Creator if available by default (mandatory attribute) [equate with Resource point of contact] |
| FDOF rightsRecord | "license":{text or URI}Or  <br>"conditionsOfAccess":{text or URI} | This is a pointer to a resource that specifies access permissions. Include: FDOF licenceConditions: that links to one or more formal specifications about licences such as CC-x; FDOF transactionRecord: a resource that includes contractual information. |
| FDOF ScientificDomain | "keywords":[{string} or schema:DefinedTerm] | indicator of the scientific domain the FDO refers to. This ensures compliance with the FAIR principles, which are per definition applicable at the domain level. This attribute is required since different mandatory attributes may be required at the domain-level. |
| Profile | "subjectOf"/"dcterms:conformsTo": {identifier} | The Kernel metadata profile is a schema that determines the attribute requirements for FDO metadata beyond the base requirements. In the FDO world, the kernel profile specifies Kernel information about the resource associated with an identifier. Schema.org does not have a 'conformTo' property so follow DCAT v3 using the Dublin Core Terms property. |
| FDOF digitalObjectType | "@type":{schema.org type} | The kind of resource associated with an identifier. The type implies a schema that dictates the format, information model, and profile conventions for the resource representation contained in the identified digital object. Use appropriate Schema.org type for \@type property, the additional type should be from a controlled vocabulary. |
| | "additionalType":[{schema:DefinedTerm or URI}, ...] | Expect to use a CDIF recommended vocabulary here |
| RDA dateCreated | "datePublished": {date time} | Date (and optional time) the Digital object was created|
| RDA dateModified | "dateModified" : {date time} | If the DO bit sequence is mutable, specify the last date/time of object modification. Must be consistent with etag and current version number. |
| RDA version | "version" : {string} | If tracked, a version for the object, which must follow a total order. Mandatory for all objects with at least one predecessor version. |
| RDA digitalObjectLocation | "url":{URL} | If the FDO has a digital representation, it is mandatory that the PID record specifies the location where the FDO can be retrieved, either as an URL or a PID. This is URL in a metadata record for which the target resource is a digital object, or the contentURL or accessURL if the target resource is a non-digital object with one or more distribution representations. Since FDO PID identifies a digital object, there is only one distribution,so use the simple schema:url. |
| FDOF operationInfo | Not implemented by CDIF v1.0 | Some communities want to include a payload information such as a thumbnail image in the case of DiSSCo's Digital Enhanced Specimen FDO. |

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/profilesoverview.md

# Overview of CDIF Profiles

# Profile Content

A CDIF profile is a set of recommended common metadata to be provided in support of a function which implements the FAIR principles, sufficient for use across domain and infrastructure boundaries. The profiles do not describe comprehensive sets of metadata – every FAIR resource and domain is different, and may require specialized metadata description.

Each CDIF profile has a stated purpose and set of requirements. Based on this purpose and the requirements, the profile is represents is an implementation-independent conceptual model. To make the profile useable, CDIF recommends a specific implementation. In some cases there might be more than one such implementation, based on the existing culture of practice. Regardless, the conceptual model is consistent across all implementations. This conceptual model is documented here for each profile in text, listing the required information items, in some cases supplemented by a formal UML model.

For technical use, a set of artefacts is made available for each profile implementation, published in a GitHub repository. These artefacts include:
1. A specification of all implemented classes, properties, and datatypes in a text document labeled “Implementation Guide.” This serves as the core documentation of what each implemented profile contains.
2. A JSON Schema for validating JSON instance documents, and for helping developers understand what is included in the profile and requires or is available for support in applications. Because the implementation uses JSON-LD, these JSON schema require instance documents to be in compacted form (see [CDIF profiles metadata validation](https://github.com/Cross-Domain-Interoperability-Framework/validation/blob/main/docs/CDIF-profiles-metadata-validation.md))
3. A set of SHACL rules for RDF validation of JSON-LD instances, and to help Linked Data developers understand what is available within a CDIF graph. The SHACL rules can be used to validate metadata instances in any JSON-LD serialization (compacted, flattened, expanded)
4. A set of example instances, showing how the conforming metadata should appear in JSON-LD.
5. A JSON Framing document. This is a special JSON-LD document that maps JSON-LD keys to a particular compacted JSON structure, in this case the structure expected by the CDIF JSON schema. This framed format is a typical JSON hierarchical tree structure with nested inline properties, typically much easier for humans to understand. Framing allows any instance document to be validated with the JSON schema. Each profile repository also includes a python program (FrameAndValidate.py) that takes a JSON-LD document as input, applies the framing document and validates with the JSON schema in that repository. This is documented in the repository readme.md file.
6. For those profiles which have been implemented as a UML model, hyper-linked field-level documentation will be made available as an html document, connecting specific classes to their expression in implementation artefacts such as SHACL and JSON Schema, as well as in a version of the model expressed in the XMI interchange format.


# Overview of Profiles in Version 1.1

This section provides a brief overview of the currently targeted profiles. More details are presented in subsequent sections.

## Core
The CDIF Core profile defines the mandatory and optional base properties for any CDIF metadata record, implemented as JSON-LD using the schema.org vocabulary.  The Core profile release repository is here: [https://github.com/Cross-Domain-Interoperability-Framework/profile-core](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/README.md)

Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/cdifCoreStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/CDIFCoreImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/coreRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/blob/reviewRevision202606/cdifCore-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-core/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCore/index.html)

## Data Discovery
 The Discovery profile defines optional properties for documenting spatial or temporal extent, and simple documentation of variables specified in a resource. This recognizes that there are a variety of resources of interest that might not have relevant spatial or temporal extent, and might not explicitly define variables with values. The Discovery release repository is here: [https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/README.md)
 
 Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/cdifDiscoveryStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/CDIFDiscoveryImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/discoveryRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/blob/reviewRevision202606/cdifDiscovery-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-discovery/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDiscovery/index.html)

## Data Description
The CDIF Data Description profile defines metadata elements for documentation of variable value domains, statistics aggregating variable values, physical data file layout, and roles of variables in a dataset (e.g. identifier, measure, attribute).  The Data Description release repository is here: [https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/README.md)

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/cdifDataDescriptionStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/CDIFDataDescriptionImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/dataDescriptionRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/blob/reviewRevision202606/cdifDataDescription-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-datadescription/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataDescription/index.html)

## Codelist

The CDIF Codelist profile defines how controlled vocabularies and classification schemes are represented as SKOS ConceptSchemes in JSON-LD. The profile composes skos:ConceptScheme and skos:Concept with CDIF-specific requirements inherited from cdifCore.  Concept properties include a preferred label, bidirectional hierarchy, notation.  CDIF core metadata properties are included on the ConceptScheme. The key feature of the codelist is specification of the 'notation' for a concept -- the strings that actually appear in data, along with a human-readable lable conveying the meaning of the code.

The implementation uses the SKOS (Simple Knowledge Organization System) vocabulary with JSON-LD serialization. This profile aligns with the approach described in ['Modelling of Eurostat's Statistical Classifications in ShowVoc'](https://cros.ec.europa.eu/book-page/modeling-eurostats-statistical-classifications-showvoc), but in alignment with cdifCore, the required properties from cdifCore are implemented using schema.org elements. The Codelist release repository is here: [https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/README.md)

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelistProfileStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelistImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/rules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/blob/reviewRevision202606/CDIFCodelist-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist/tree/reviewRevision202606/Examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFCodelist/index.html)

## Data Structure

This profile supports the description of reusable data structures and/or their component variables. Enumerated values for variables are described using the Codelist profile. This profile primarily uses the DDI-CDI standard. 

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/cdifDataStructureStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructureImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/dataStructureRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/blob/reviewRevision202606/CDIFDataStructure-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-datastructure/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFDataStructure/index.html)

## Concept Scheme

This profile uses SKOS to describe concept systems which are meaningful for purposes other than the representation of variable values. Domain ontologies may need to be expressed for FAIR use: this profile is intended as a supplement to ontologies described in OWL as it can be rendered using tools such as SKOSify from them, so that they are more widely accessible.

Resources:
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/cdifConceptSchemeStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/CDIFConceptSchemeImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/conceptSchemeRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/blob/reviewRevision202606/cdifConceptScheme-frame.jsonld)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-conceptscheme/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/cdifConceptScheme/index.html)

## Manifest

This profile is used to package metadata and FAIR resources, to form bundles for dissemination, archiving, etc. It can be used to render "webby" FDOs. The recommended implementation uses [RO Crate](https://www.researchobject.org/ro-crate/).

Resources: 
- [Structured JSON schema](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/cdifManifestStructuredSchema.json)
- [Implementation guide](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/CDIFManifestImplementationGuide.md)
- [SHACL rules](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/manifestRules.shacl)
- [JSON-LD framing](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/blob/reviewRevision202606/cdifManifest-frame.jsonld)
- [Transform RO-CRATE to/from CDIF](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/tree/reviewRevision202606/tools)
- [Example instance files](https://github.com/Cross-Domain-Interoperability-Framework/profile-manifest/tree/reviewRevision202606/examples)
- [Graphical view](https://cross-domain-interoperability-framework.github.io/metadataBuildingBlocks/cdif-uml-model/CDIFManifest/index.html)

## Access 

This is a general guideline for the use of the [Open Digital Rights Language (ODRL)](https://www.w3.org/TR/odrl-model/) to describe the policies for the access conditions and use of FAIR resources. This profile gives some general guidance on these important topics.

Resources: 
- [ODRL overview](https://cross-domain-interoperability-framework.github.io/cdifbook/data-access/odrloverview/)
- [ODRL Implementation](https://cross-domain-interoperability-framework.github.io/cdifbook/data-access/odrlincdif/) 

## Universals

Time, geography, and units of measure are used ubiquitously in data and metadata, and are important for the integration and use of data. This profile gives some general guidance on these important topics.

Resources: 
- [Overview](https://cross-domain-interoperability-framework.github.io/cdifbook/universals/univintro/)
- [Geography](https://cross-domain-interoperability-framework.github.io/cdifbook/universals/univgeography/)
-[Time](https://cross-domain-interoperability-framework.github.io/cdifbook/universals/univtime/)
-[Units of Measurement](https://cross-domain-interoperability-framework.github.io/cdifbook/universals/univuom/)

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/publication.md

# Metadata Publication

This section describes workflows recommended for a metadata publisher to make their metadata accessible to Web crawlers for search engines to index their resources. The figure below is a flow chart showing the decision tree to determine how to expose metadata. Numbers in the following discussion refer to numbered boxes in the diagram.

![metadatapubworkflow](./figures/fig-flowchart.jpg)

Figure. Decision graph to determine where metadata is located, from the resource publisher's perspective. Steps are numbers and referenced in text.

## Option 1. Embedded in HTML
Starting at the top (1) in the above figure, if there are HTML landing pages that describe the resources of interest, and the metadata publisher has the necessary authority to update the content of these pages, then CDIF metadata serialised as JSON-LD (see Appendix 1) should be embedded in an HTML &lt;script&gt; element in the &lt;head&gt; section of each landing page (3). The script should have the following type and profile attributes: 

<p style="text-align: center;">type="application/ld+json" profile="CDIF1.0"</p>

## Option 2. Individual Metadata File URLs
If the resources of interest do not have individual landing pages, or the metadata publisher does not have authority to update the content of landing pages, the metadata should be placed in a Web-accessible location (step 4 in the figure above). There are two common approaches:
- Each metadata record is accessed in a separate, static file with its own URL. The CDIF metadata is serialised as JSON-LD (see [Schema.org implementation](./schemaOrgImplementationpatterns.md) ). MIME type for the metadata file, returned as the Content-Type parameter in the HTTP response header, is:
<p style="text-align: center;">type="application/ld+json" profile="CDIF1.0"</p>

- Each metadata record is accessed dynamically from the server using a URL. There are various open-source metadata server systems that can be configured to deliver CDIF metadata from the server's metadata database, e.g. [GeoNetwork OpenSource](https://geonetwork-opensource.org/), [GeoPortal](https://github.com/Esri/geoportal-server-catalog), [CKAN](https://ckan.org/). The metadata retrieval URLs have different syntax depending on the software used, but typically include a metadata record identifier and a format parameter that would be used to indicate that CDIF metadata should be returned. If there is a format parameter in URL requests, its value should be '**CDIF1.0**'.

## Option 3. Metadata List File
- A collection of metadata records is gathered in one file accessed using a single URL. For CDIF, this file should contain a set of CDIF JSON-LD metadata objects, implemented as a schema.org [ItemList](https://schema.org/ItemList). See example in Appendix 1. The MIME type for the collection is:

<p style="text-align: center;">*type="application/ld+json" profile="CDIF-list-1.0"*</p>

# Find Metadata
CDIF recommends the use of sitemaps to address the questions of how crawlers find metadata to index or use. A [sitemap](https://www.sitemaps.org/protocol.html) is an XML document that a metadata crawler or harvester can access (**6** in the figure above). The basic sitemap is an XML document that is a structured list of URLs, with an optional date stamp property that should indicate when the metadata at the URL target location was last updated. The most basic CDIF recommended approach for resources that have landing pages that can be modified is Option 1 outlined above. The workflow for a harvester in this approach corresponds to existing structured data on the Web practice, with metadata conforming to the CDIF recommendations. Existing robots.txt and sitemap files can be used, and no modifications need to be made to HTTP headers provided by resource servers.

![Basic harvesting pattern](./figures/basicharvestingpattern.jpg)

Figure. Basic harvesting pattern: sitemap with locations that contain HTML documents with embedded CDIF metadata

If resources do not have landing pages, or the landing pages cannot be modified, harvesters must be provided with links to the metadata records to index. The basic approach for this next level of service is similar, but the harvester cannot assume that the metadata is embedded in the content accessed from the sitemap url/loc. The sitemap url/locs must either get the metadata document directly, or it might get the resource content directly. In the second case, a URL to get the metadata must be included in the HTTP response header. Because the basic sitemap only provides a URL, the harvester will need to check which of these options is being used. The approach using standard Web architecture is to inspect the HTTP response header. If the returned document is a CDIF metadata document, the header will have a content-type parameter with the value "*application/ld+json; profile='CDIF1.0'*" or *profile='CDIF-list-1.0'* if the document is an itemList with multiple metadata records. The harvester should get the content at the sitemap url/loc and use that. If the content-type has a different value, then the header should have link element with *rel='describedby'*, *type='application/ld+json'*, and *profile='CDIF1.0'* or *profile='CDIF-list-1.0'*. In this case, the harvester will GET the content at the link href and use that. Inclusion of the describedby link in the HTTP header is the pattern used by Signposting.

Other [Signposting links](./signpostinglinkrel.md) could be inserted into the HTTP response headers (or HTTP landing pages if they exist) if Web site administrators allow. This can provide additional value for clients implementing signposting.

![Harvesting pattern for locations that do not have embedded metadata scripts](./figures/harvestnoembeddedscript.jpg)

Figure. Harvesting pattern for locations that do not have embedded metadata scripts. Either the url/loc content is a metadata document (JSON-LD, CDIF profile), or there is a Signposting link with *rel=describedby* in the HTTP head. To indicate that this is not a standard sitemap, the robots.txt link to the sitemap should identify CDIF1.0 as the userAgent.

Note that in this second case, the sitemap url/loc locations will get content that is not HTML. A non-CDIF aware harvester will be expecting HTML (or indexable text) content, and this might cause problems. Harvesters will generally find the sitemap using a link from a [robots.txt](https://datatracker.ietf.org/doc/rfc9309/) file placed in the root of the server containing the sitemap and metadata. In the robots file, the user agent value can be used to indicate a sitemap link for CDIF-aware agents in cases for which the sitemap links are not to pages that have embedded CDIF metadata &lt;script&gt; elements. If the harvester accesses a sitemap under this user agent, the url/loc location content should be processed as outlined in the last paragraph.

<p style="font-family:courier;">User-agent: CDIF1.0</p>
<p style="font-family:courier;">Sitemap: http://www.example.com/CDIFsitemap.xml </p>

Based on these recommendations, metadata generated using the CDIF content and serialisation can be found and harvested by agents using standard off-the-shelf Web technology.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/publishingmetadata.md

# Publishing Metadata

The use of standardised metadata to describe resources is one facet of discoverability, but mechanisms to make these metadata descriptions discoverable by search applications or other machine agents is also necessary. Search applications harvest metadata to index and present in search results. In other cases a machine agent might have an identifier for a resource on the Web and want to get its metadata to learn about the content and capabilities of the resource.

## Signposting
Signposting is an approach to discovering the content and capabilities of resources accessed by resolving URIs on the Web. Like the FAIR Digital Object framework, it starts with an identifier that can be resolved, and uses typed Web links ([IETF RFC8288](https://datatracker.ietf.org/doc/html/rfc8288)) and [IANA registered relationship](https://www.iana.org/assignments/link-relations/link-relations.xhtml) types to enable an agent to discover what is identified and navigate to metadata with more information. These signposting links can implement the linking requirements of the [Fair Digital Object Framework](https://www.slideshare.net/hvdsomp/fair-signposting-a-kiss-approach-to-a-burning-issue). The CDIF metadata requirements outlined below include recommended or optional properties necessary to create a FDO PID Kernel information record (FDOFIdentificationRecord in Figure 1, below) as recommended by the Research Data Alliance (RDA)([Weigel et al. (2018)](https://doi.org/10.15497/RDA00031) ). Signposting can be used to implement FDOF requirements, and in the following implementation discussion we outline how Signposting is compatible with CDIF. The mapping from the PID Kernel information record to the CDIF metadata schema.org recommended implementation is shown in [PID kernel mapping](./pidkernel.md). Mapping from Signposting link relation types to CDIF metadata elements is shown in [Signposting link mapping](./signpostinglinkrel.md).

![FDOF-CDIF metadata relations.](./figures/fdof-cdif-relations.jpg)

Figure 1. FDOF-CDIF metadata relations.

## Search Engines
One of the drivers for the success of the World Wide Web is the emergence of search applications that use various mechanisms to traverse the Web, find Digital Objects of interest, analyse those objects to extract information about their content, and create indexes that support user searches for resources of interest. Creators and providers of Web resources (publishers) seek to increase visibility and usage of their published resources by assuring that search engines (aggregators) find and index their products. This section outlines various approaches used to make metadata accessible to search engines.

**Finding documents to index**: Web-crawling is still an important approach to finding and indexing resources on the Web, and this approach is supplemented by Signposting. A different and widely-used approach is the sitemap, which is a list of Web locations (URLs) for files that a hosting agent wants search engines to index.  Many search engines enable providers to register sitemap locations. Alternatively, a widely-used convention on Web servers is to place a 'robots.txt' file in the root directory of a Web site. This file contains links that point to one or more sitemaps that should be indexed.

**Getting the metadata**: Once a crawler for a search application finds a document that should be indexed, it must determine if there is structured metadata to index, and what conventions the metadata uses. Possible approaches:

1. Each resource has an HTML landing page that describes the resource for human users, and contains embedded metadata for machine clients. Metadata can be embedded in landing pages using the HTML &lt;script&gt; element, in alignment with the Data on the Web Best Practices, specifically [section 8.2, Metadata](https://www.w3.org/TR/dwbp/#metadata) (See Example 1). This approach requires that each published resource has a human-readable landing page, intended to be the target of search by human users. Scripts are normally embedded in the &lt;head&gt; section of an HTML document. The &lt;script&gt; element has at minimum a 'type' attribute that provides a MIME-type specifying the type of script. 

![example1](./figures/ex1-jsonldembededinhtml.jpg)

Example 1. A JSON-LD metadata object embedded as a script in an HTML document.

2. Metadata can be embedded in the HTML &lt;head&gt; section of a landing page using HTML &lt;meta&gt; elements, which have a 'name' attribute that can be used to identify different metadata properties (see Example 2). This approach has been implemented by some off-the-shelf repository software (e.g. Dataverse). The HTML &lt;meta&gt; elements are intended to describe the HTML document that contains the [&lt;meta&gt; element](https://www.w3.org/TR/2011/WD-html5-author-20110809/the-meta-element.html), not some external resource that the Web page is about. CDIF recommends against this approach and suggests using the script approach (No 1 in this list) instead because that is more widely used and allows richer metadata content to be included. 

![example2](./figures/ex2-htmlmetatags.jpg)

Example 2. HTML meta tags with metadata about a resource.

3. Metadata can be linked from the landing page using the HTML &lt;link&gt; element in the &lt;head&gt; section to provide a Web locator (URL) that can be used to retrieve a full metadata document about the described resource. The link element has the "rel='describedby'" attribute to indicate that the link is to metadata; a 'type' attribute to provide the MIME type of the target metadata record; and optionally a 'profile' attribute to identify specific metadata conventions. Note that multiple links could be provided to different metadata views, e.g. a CDIF record, a PID Kernel record, a FDOFidentifierRecord, etc. This approach depends on Web-crawlers to identify and follow these links to get the metadata that the provider wants indexed. This is one of the [Signposting approaches](https://signposting.org/).

4. The server providing the resource can be configured to include &lt;link&gt; elements in the [HTTP response header](https://tools.ietf.org/html/rfc8288) that indicate the location of machine-actionable metadata describing the subject of the URL target. As in the HTML link approach, these links would have a "rel='describedby'" attribute to indicate that the link is to metadata, a 'type' attribute to provide the MIME type of the target metadata record, and optionally a 'profile' attribute to identify specific metadata conventions. The advantage of this approach is that the HTTP response header links can be provided for any resource that has an HTTP URL, so links to metadata can be accessed for non-textual resources that do not have an associated HTML landing page. If the download size for the resource is large, a client can use the HTTP 'head' request to access this header information without downloading the [entire file](https://tools.ietf.org/html/rfc7231#section-4.3.2). This approach would enable indexing of large resource collections that have a single landing page, but for which the individual resources do not have a landing page, e.g. a STAC catalogue. The downside is that many client applications do not use the [HTTP header information](https://www.w3.org/TR/ldp-bp/#use-case-2-providing-metadata-in-both-http-headers-and-html-body). This is a second Signposting approach. CDIF recommends this approach for resources that do not have landing pages; see [implementation recommendations](queryabledistributions.md).

5. A sitemap can point directly to metadata documents in formats that the search engine can parse. With the basic sitemap XML schema, all metadata would need to conform to a single profile. In the implementation section below, the CDIF proposes using an extension to the sitemap scheme that allows labelled links to the indexing targets.

6. Another option is for the sitemap to provide a URL that retrieves a document containing a collection of metadata records, something like the US Government Data.gov [Project Open Data Catalog](https://project-open-data.cio.gov/v1.1/schema/catalog.json), or [Ocean Info Hub graph first approach](https://book.oceaninfohub.org/indexing/graphpub.html), with individual records providing CDIF profile metadata.

## How Do Harvesters Know Where to Look?
- Publishers register metadata services with a harvester, e.g. by providing a URL to GET a sitemap or other metadata catalogue document, e.g. an [OpenGeospatial Consortium (OGC) Record collection (catalogue)](https://docs.ogc.org/DRAFTS/20-004.html#sc_record-collection-overview). 
- Server robots.txt has link to sitemap.xml file; The sitemap.xml lists Web locations that a crawler should
index.

Once the harvester has a URL for a location to index, how do they know where the metadata is relative to that location? Possible approaches:

- Try a [HTTP HEAD request](https://www.rfc-editor.org/rfc/rfc9110#HEAD) on the URL and inspect. If the Content-Type header value is a known metadata type and profile, then the URL will get a document containing a single metadata record that can be indexed. Failing that, the client can look for links in the HTTP response header; if there is a link with rel='describedby', with a known type and profile, get the content at that link. 
- GET the content at the URL. Look for a &lt;script&gt; element with a known type and profile. Failing that, look for elements with rel='describedby' and a known type and profile, then get the content at that link. This general procedure can be simplified if the sitemap or other catalogue the harvester is iterating through
provides labelled links.

## What Does the Harvester Do with the Metadata?

There are many possible approaches a client application could use to extract the information it needs from a metadata record. The simplest and likely most accurate approach is for the metadata to conform to a profile that the application is programmed to parse, and to communicate that profile conformance to the application. This entails two requirements. The profile must be documented in a way that allows software developers to write code to parse metadata conforming to the profile, and the profile must have an identifier that can be used to assert conformance.

- The use of &lt;script&gt; or &lt;link&gt; elements (in the HTTP or HTML header) allows metadata to be offered following multiple specifications with the 'type' and 'profile' attributes used to identify the [particular conventions](https://www.w3.org/TR/dx-prof-conneg/#dfn-profile) (Example 3). Minimally, the metadata record should assert the specification used to generate the record in a metadata property.

![example3](./figures/ex3-scriptwithtype.jpg)

Example 3. Script with a type parameter in the MIME-type string

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/queryabledistributions.md

# Queryable Distributions

This section provides details for documenting online data distribution approaches.

## Data Provider Conventions

**File download distribution**. In the simplest and still common file-based data access scenario, the dataset distribution information in a metadata record includes a link (URL) that will get a file containing the actual resource content in a particular format. The format and information model for the file content must be specified in the distribution object in the metadata. The HTTP protocol is used to GET a resource. Given the view that an API specifies the functions offered and constrains the content of messages transmitted between a client and the agent, this simple file download is not considered an API.

**Service based distribution**. An API builds on a basic communication protocol (e.g. HTTP) by defining functionality and formatting to enable providing the specific data a user requires. This might involve filtering, subsetting, or various transformations for e.g. schema mapping, aggregating or anonymizing data. The focus here is on Web APIs that provide data using a URL for the endpoint location (the server that implements the data access protocol), with parameters to specify the particular data requested. The query parameters might be appended to this base URL as part of the URL, or provided as a message with the request. Metadata content requirements:

- **Service type** -- specify the kind of service. Ideally this should be a resolvable identifier. Currently there is no widely adopted registry for serviceType identifiers, in large part because services might be defined at different levels of granularity, and classifications might focus on function, data formats, thematic content, security, or other aspects of the service definition. For interoperability, there must be an external arrangement between data providers and consumers on the strings that will be used to specify service types. Cardinality: 1..*.
- **Service description document** -- many service implementations include provision for a document that provides a machine-actionable description of a service instance. Examples include OpenAPI documents, OGC Capabilities documents. Software designed to utilise a particular service type will typically include functionality to parse such a description document and engage with the service endpoint. If such a document is available for the service instance providing the resource distribution, it should be included in the distribution metadata. Cardinality (0..1, conditional, required if it exists) 
- **Endpoint URL** -- the base location identifier (URL) through which the service is accessed. If a service description document is provided, the location of the service endpoint would be the other piece of information needed; the endpoint location might be related to the location for the service description document and thus not required to be specified separately. Cardinality (0..1).
- **Access constraints** -- Description of access privileges required to use the API, e.g. registration, licensing, payments. Note that access constraints applying to any distribution of the resource should be specified in the access constraints for the resource description as a whole.

If a service description document is not available, some basic information about the API should be provided in the metadata. The operations offered by the service and the output formats (serialisation scheme and information model) are typically defined in the service specification, and would thus inhere in the service type identifier for clients that recognise the service type. These might be optional in the service type specification, with choices for what it offered specific to a particular endpoint, in which case they should be asserted in the metadata for the particular endpoint.

- **Operations** - specify the functions offered by the service endpoint
- **Output formats** - specify the output formats (serialisation scheme and information model) for
service response documents.
- **URL template** - A template for an HTTP service request that indicates how to invoke the service. The
URL template must follow the conventions specified in [IETF RFC6570](https://datatracker.ietf.org/doc/html/rfc6570). Parameters that are specified
by the user when invoking the service are enclosed in curly brackets ('{ }'). Note that the URL
template must be consistent with the specified service type.
- **Parameters** - some description of the URL parameters that can be specified in the service request
URL. This should include a description of what the parameter does, what data type is used, and the
cardinality for the parameter. If the parameter is populated from a controlled vocabulary, some
specification of the allowed values should be provided, either as an enumerated list or a link to a
vocabulary that will be recognised by users.

## Metadata Provider Conventions

Metadata providers offering APIs to search metadata catalogues can be considered a special case because they play a 'middleware' role between resource providers and resource consumers. The only real difference is in the intention of the content offered by the API. The resource they offer is data that is about other data, but the distribution description fits into the above content model. The service type would need to indicate that the API is for discovering information about resources (potentially in some thematic scope). The operations would necessarily include a search operation. The output formats would be the metadata schemes (and optional profiles) offered for service responses, e.g. ISO19115-3 MCP profile, ISO19139 INSPIRE profile, schema.org CDIF profile, DCAT-AP. URL template parameters would include the various properties that are queryable.

## Data User Conventions

To identify an API that an application can work with, metadata for the application must specify what formats are acceptable for input data, and the interface(s) used by the application to request input data in that format. The software input file format will be matched with the output formats and the implemented communication protocols will be matched with the service types offered by resource distributions to determine where interoperability is possible.

- **Input file format** -- indicate input formats understood by the application. For interoperability, the format must be specified using strings established by convention between providers and consumers. Use of generic MIME-Types is not sufficient in most cases as these are quite general and can result in data-API matches that don’t actually work.
- **Interface specification**. A communication protocol defines how messages are transmitted between a client and server. The software metadata must specify the application interface(s) (API) that it implements to interact with services providing resources for operation of the software. The API specifies the communication protocol that is used and the formats for requests and expected responses that an application uses to access data from a server.
- **Execution environment**. The software environment needed for operation of the application, e.g. operating system, online/cloud.

For applications operating in a single desktop or local-area network environment, operating systems like Windows, AppleOS, or Linux offer various communication protocols, and applications use various bespoke drivers to implement connection and communication. The simplest case is file-based access using the standard operating system file-open dialogs, and the ‘Interface specification’ is simply ‘local file system’. File-based data retrieval using a URL is similarly simple and ‘Interface specification’ is simply ‘HTTP’. The encodingFormat is the critical information to match data sources with applications in these cases.

The data source might be a relational database like PostgreSQL, MySQL, or any of a variety of noSQL datastores like SOLR, HaDOOP, or MongoDb. The ‘Interface specification’ in this case only needs to indicate that the application has drivers necessary to acquire data from one of these data sources by identifying the data source by name. The encodingFormat used to transmit data between source and consumer is invisible to the user in this case, so the input file format is not required to be specified.

An application might access data via a WebAPI-- using interfaces communicating via the internet and based on HTTP operations (GET, POST, PUT, DELETE), or by tunnelling operation requests embedded in HTTP requests (e.g. OGC GetCapabilities). An application might depend on some particular operations or request parameters (e.g. file formats or profiles), in which case the application metadata ‘Interface Specification’ should be specific to these requirements. Alternatively, the software might operate with any data source that implements a particular interface (API). In this case the software metadata does not need to specify particular file formats or request parameters, these are built into the software and the interface definition. For a particular data access connection, the dataset distribution needs to specify the correct request parameters to get particular data (see [Service based distribution](coreSchemaImplementationNew.md#service-based-distribution) ).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/recommendations.md

# Metadata Recommendations

CDIF metadata recommendations are packaged in a [set of profiles](https://cross-domain-interoperability-framework.github.io/cdifbook/background/structure/#summary-of-cdif-profiles-and-recommendations). Each profile includes:
1. A Content model that specifies the information expected to be included in any metadata record, with required, recommended and optional content items. Each profile description starts with a description of its content model, e.g. for the [core profile](https://cross-domain-interoperability-framework.github.io/cdifbook/metadata/core/#information-model)
2. A JSON-LD serialization for that content using the Schema.org vocabulary to define the fields in a metadata record, e.g. [Core profile JSON-LD serialization](./coreSchemaImplementationNew.md), and an [implementation using the DCAT rdf vocabulary](./dcat.md)
3. Tools for validating metadata instance documents, including JSON schema, SHACL rules, a JSON-LD framing document, and python code to run validation. 

Each CDIF profile is housed in a github repository containing an implementation guidance document, JSON schema, SHACL rules, a JSON-LD framing document, and a subdirectory containing examples. 

An additional critical part of the recommendations is description of [Workflows to publish CDIF metadata](./publication.md) so that is can be found and indexed by search providers using standard web technology.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/schemaOrgImplementationpatterns.md

# Schema.org Implementation of CDIF Metadata

JSON-LD has been chosen as the recommended serialization format for CDIF metadata following our principle to use existing mainstream technology. The JSON format is widely used for data serialization and popular with developers. JSON-LD adds additional syntax for the representation of linked data, compatible with existing JSON implementations so that integration with existing applications is relatively frictionless. Many metadata providers are using the [schema.org](https://schema.org/) vocabulary with JSON-LD serialization for metadata publication and interchange. Use of this format provides a low barrier to entry for data providers.

The JSON syntax is defined by the [ECMA JSON specification](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/), and JSON-LD is specified in the [JSON-LD 1.1 recommendation](https://www.w3.org/TR/json-ld11/) from the World Wide Web Consortium (W3C). This serialization is designed for linked data applications that will translate the JSON into a set of {subject, predicate, object} triples that can be loaded into an RDF database for processing. The JSON-LD context binds JSON keys to URIs for more precise semantics, and the use of URIs to identify entities and property values in the metadata will maximize the linkage with resources on the wider web to build an ever-expanding global knowledge graph.

The metadata about the resource has properties about the resource like title, description, responsible parties, spatial or temporal extent (as outlined in the [Metadata Content Requirements](./contentmodel.md) section).

In a harvesting/federated catalog system some metadata about the metadata is useful to keep track of where metadata came from, what format/profile it uses (harvesters need this to process), and update dates [see Metadata Content Requirements](./contentmodel.md). Unambiguous expression of this information requires making statements about a metadata record distinct from the thing in the world that the metadata describes. In an RDF framework, this requires a distinct identifier for the metadata record object that will serve as the subject for these triples.

Schema.org includes several properties that can be used to embed information about the metadata record in the resource metadata: [**sdDatePublished**](https://schema.org/sdDatePublished), [**sdLicense**](https://schema.org/sdLicense), [**sdPublisher**](https://schema.org/sdPublisher), but lacks a way to provide an identifier for the metadata record distinct from the resource it describes, to specify other agents responsible for the metadata except the publisher, or to assert specification or profile conformance for the metadata record itself.

In the RDF serialization, Schema.org metadata records are [JSON-LD node objects](https://www.w3.org/TR/json-ld/#node-objects), and include an "@id" keyword with a value that identifies the node, analogous to a primary key in a relational database.  This identifier can be interpreted to represent a thing in the world that the metadata record (the 'node') is about, or to represent the metadata record (a JSON object) itself.

To avoid this ambiguity, CDIF adopts the convention that the schema.org identifier property is used to identify a thing in the world that is the subject of the JSON-LD node.  The identified thing might be physical, imaginary, abstract, or a digital object.  The JSON-LD \@id property identifies a node in a graph, which is an abstract object. As a URI the \@id URI is expected to dereference to produce a JSON-LD object containing the properties that are attached to the graph node. Given this convention, when the metadata record is processed, the processor should use the schema:identifier as subject of triples about the subject of the metadata record to avoid ambiguity.  In addition, this convention would suggest that if a schema:identifier property is present, the \@id property should be interpreted to identify the JSON object that is the representation of the node in the knowledge graph.

Statements about the metadata record (the JSON object) as a distinct entity should be made using a separate identified node object. This node object is embedded in the resource metadata using the `schema:subjectOf` property (Example 1 below), or published as a separate node in the graph (Example 2 below). The embedded node uses `@type: ["schema:Dataset"]` with `schema:additionalType: ["dcat:CatalogRecord"]` to indicate that it functions as a catalog record, and links back to the resource via `schema:about`. Note that this approach parallels the [DCAT CatalogRecord](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog_Record).

## JSON-LD Context

The CDIF implementation requires that the `@context` be an object declaring namespace prefixes used in the metadata record. At minimum, the `schema`, `dcterms`, and `dcat` prefixes must be declared:

```json
  "@context": {
    "schema": "http://schema.org/",
    "cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
    "dcterms": "http://purl.org/dc/terms/",
    "geosparql": "http://www.opengis.net/ont/geosparql#",
    "spdx": "http://spdx.org/rdf/terms#",
    "time": "http://www.w3.org/2006/time#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "prov": "http://www.w3.org/ns/prov#"
  }
```

Additional prefixes may be needed depending on which optional properties are used (e.g. `dqv`). Because CDIF uses prefixed property names (e.g. `schema:name` rather than `name`), the context must map each prefix to its namespace IRI.

## Catalog Record (subjectOf)

The metadata record information is embedded using `schema:subjectOf`. The CDIF implementation types the catalog record node as `schema:Dataset` with `schema:additionalType` of `dcat:CatalogRecord`:

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "dcterms": "http://purl.org/dc/terms/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "spdx": "http://spdx.org/rdf/terms#",
    "ex": "https://example.com/99152/"
  },
  "@id": "ex:URIforNode1",
  "@type": ["schema:Dataset"],
  "schema:identifier": {
    "@type": "schema:PropertyValue",
    "schema:propertyID": "https://registry.identifiers.org/registry/doi",
    "schema:value": "10.1234/example",
    "schema:url": "https://doi.org/10.1234/example"
  },
  "schema:name": "unique title for the resource",
  "schema:description": "Description of the resource",
  "schema:dateModified": "2017-05-23",
  "schema:license": ["https://creativecommons.org/licenses/by/4.0/"],
  "schema:url": "https://example.com/resource-landing-page",
  "schema:subjectOf": {
    "@id": "ex:URIforNode2",
    "@type": ["schema:Dataset"],
    "schema:additionalType": ["dcat:CatalogRecord"],
    "schema:about": {"@id": "ex:URIforNode1"},
    "schema:sdDatePublished": "2017-05-23",
    "dcterms:conformsTo": [
      {"@id": "https://w3id.org/cdif/core/1.1/"},
      {"@id": "https://w3id.org/cdif/discovery/1.1/"}
    ]
  }
}
```
Example 1.  Metadata about the metadata embedded via subjectOf.

This can also be implemented in a more flattened form as a graph with a separate node for the "schema:Dataset" with schema:additionalType" "dcat:CatalogRecord".  This serialization will validate with the SHACL rules but not the JSON schema unless the instance document is framed using the CDIF framing documents in the release repositories.

```json
{
  "@context": {
    "schema": "http://schema.org/",
    "dcterms": "http://purl.org/dc/terms/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "ex": "https://example.com/99152/"
  },
  "@graph": [
    {
      "@id": "ex:URIforNode1",
      "@type": ["schema:Dataset"],
      "schema:identifier": "ex:URIforDescribedResource",
      "schema:name": "unique title for the resource",
      "schema:description": "Description of the resource"
    },
    {
      "@id": "ex:URIforNode2",
      "@type": ["schema:Dataset"],
      "schema:additionalType": ["dcat:CatalogRecord"],
      "schema:about": {"@id": "ex:URIforNode1"},
      "schema:sdDatePublished": "2017-05-23",
      "dcterms:conformsTo": [
        {"@id": "https://w3id.org/cdif/core/1.1/"},
        {"@id": "https://w3id.org/cdif/discovery/1.1/"}
      ]
    }
  ]
}
```

Example 2. Metadata about metadata as a separate graph node.

The distinct identifier for the metadata record allows statements to be made about the metadata separately from statements about the resource it describes. The catalog record node requires `@type`, `schema:additionalType`, `@id`, `schema:about`, and `dcterms:conformsTo`.

## Conformance URIs

Each CDIF building block defines a conformance URI that must be listed in the catalog record's `dcterms:conformsTo` array. The URIs follow the pattern `https://w3id.org/cdif/{scope}/{version}/`. A CDIFDiscovery-conformant record must declare at minimum:

| Building block | Conformance URI |
|---|---|
| cdifCore | `https://w3id.org/cdif/core/1.1/` |
| cdifOptional (Discovery) | `https://w3id.org/cdif/discovery/1.1/` |

Extended profiles add additional conformance URIs (e.g. `https://w3id.org/cdif/datadescription/1.1/`, `https://w3id.org/cdif/provenance/1.1/`).

JSON keys prefixed with '@' are keywords defined in the [JSON-LD specification]( https://www.w3.org/TR/json-ld11/#keywords) (see table below)

 | Keyword  |   Description|
 |-----------|-------------|
 | \@context |  The value must be an object that maps namespace prefixes to their IRI expansions. CDIF requires at minimum `schema`, `dcterms`, and `dcat` prefix declarations. Additional prefixes (e.g. `geosparql`, `prov`, `dqv`, `time`) are needed when using properties from those namespaces. |
|  \@id    |    A string that identifies the subject of the assertions in the JSON object that contains the \@id key.|
|  \@type   |   An array of type identifiers for the JSON object. In CDIF, the array must include `schema:Dataset`. Additional schema.org types from the allowed set may also be included. Values use the `schema:` prefix (e.g. `schema:Dataset`, `schema:CreativeWork`). The `schema:additionalType` property should be used for types from other vocabularies (e.g. `dcat:CatalogRecord`). |


# Implementation Patterns

All property names use namespace prefixes as declared in the `@context` (e.g. `schema:`, `dcterms:`). The `schema:` prefix is required for all schema.org properties. The CDIF JSON-LD implementation uses a hierarchical JSON structure, and CURIE syntax to abbreviate URIs using prefixes defined in the JSON-LD context.  The implementation does not map un-prefixed JSON keys to URIs, rather prefixes a namespace abbreviation on the key label to represent the URI.  This enables using standard JSON schema to validate documents and avoids confusion about the vocabulary origin of keys used in the JSON.

-   cdifConceptOrTerm. {label, schemename, conceptURI, schemeURI}. This is a pattern used for property values that are concepts defined in a controlled vocabulary, ontology, or similar semantic artefact. The current implementation allows two approaches-- use schema.org DefinedTerm or skos:Concept.  In DefinedTerm values have a `schema:name` (label meaningful to humans), `schema:inDefinedTermSet` (identifies the source semantic resource), `schema:identifier` (a PropertyValue with the concept URI), and `schema:termCode` (a short code for the concept). In the cdif skos:Concept, values have a `skos:prefLabel` (label meaningful to humans), `skos:inScheme` (identifies the source semantic resource), `schema:identifier` (a URI), and `skos:notation` (a short code for the concept).

-   Identifier. Identifiers can be inserted as simple string literals. If the identifier can be provided as a string literal that is resolvable and for which the identifier scheme is evident, that is all that is required. If the identifier scheme is not well known, or a separate resolver must be used, use the schema:PropertyValue to provide additional information. The `schema:propertyID` specifies the identifier scheme. CDIF recommends using scheme identifiers from [https://registry.identifiers.org/registry/](https://registry.identifiers.org/registry/). The `schema:value` provides the identifier as a string value. If the identifier can be resolved on the web, the `schema:url` provides a resolvable URL.

-   Agent. This pattern is for specifying an Agent in the PROV sense: An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent\'s activity. Agents can be persons, organizations, or software-defined actors. Agents have a `schema:name` for human recognition, a type (schema:Person, schema:Organization), an `@id` identifier, `schema:contactPoint` and `schema:affiliation`. Machine agent contact points should be the accessible human who operates the environment running the machine agent. This pattern is used for hard-typed roles in the CDIF implementation-- schema:creator, schema:maintainer, schema:contributor, schema:provider. Other roles can be documented using the [schema.org role pattern](http://blog.schema.org/2014/06/introducing-role.html) in the schema:contributor property. Note that `schema:creator` uses the JSON-LD `@list` wrapper to preserve author ordering.

-   DistributionObject {contentUrl, encodingFormat, dcterms:conformsTo, distributionAgent}. This pattern specifies information for implementing machine access to a DigitalObject. Includes a URL (`schema:contentUrl`) for the web location at which the DigitalObject can be accessed, the specifications or profiles to which the serialization and content of the object conform using `dcterms:conformsTo` (an array of objects with \@id), the format of the digital object content (`schema:encodingFormat`), and the Agent responsible for the distribution platform (`schema:provider`). The `@type` must be an array containing `schema:DataDownload`.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/signpostinglinkrel.md

# Mapping from Signposting Relations to CDIF Metadata Elements

The Signposting approach embeds links in HTML pages or in the HTTP header that is included in the response to HTTP GET or HEAD requests. These links provide some basic metadata information, as well as links to more complete metadata, possibly in various formats or [profiles](https://signposting.org/FAIR/#level1). Given an identifer that can be derferenced using a server that implements signposting, an agent can obtain some information about the resource(s) that can be accessed by dereferencing the identifier. If a provider has generated CDIF metadata records, they hae sufficient information to generate signposting links. If they can add HTML <link> elements in landing pages, or HTTP <link> elements in the server GET and HEAD responses, then implementing signposting is an easy win, providing value for some users. The table below show the mapping from CDIF metadata elements to the targets for signposting links with each REL types. 

Signposting Relation Type | CDIF schema.org element | Description | 
------------------ | -------------------- | ----------------- | 
 |author | "creator"/"@id" | The target of the link is a URI for an author of the resource that is the origin of the link. | 
 |cite-as | "@id" | The target of the link is a persistent URI for the resource that is the origin of the link. | 
 |describedby | "subjectOf"/"@id" | The target of the link provides metadata that describes the resource that is the origin of the link. | 
 |describes | "subjectOf"/"about"/"@id" | The origin of the link is a resource that provides metadata that describes the resource that is the target of the link. It is the inverse of the describedby relation type. | 
 |type | "@type": {schema.org type}; use "additionalType" for more specific typing | The target of the link is the URI for a class of resources to which the resource that is the origin of the link belongs. | 
 |license | "license"/"@id" | The target of the link is the URI of a license that applies to the resource that is the origin of the link. | 
 |item | "relatedLink"/ /{"linkRelationship": "hasPart",<br>"target": {<br>"url":"http://someurl...", <br>"contentType": "resource type of the item"}} | The origin of the link is a collection of resources and the target of the link is a resource that belongs to that collection. It is the inverse of the collection relation type. In CDIF, contentType and encodingType properties can provide details about the kind of linked collection item. | 
 |collection | "relatedLink"/ / {"linkRelationship": "IsPartOf", <br>"target": {<br> "url":"http:someURL.."<br> "contentType": "Collection"}} | The origin of the link is a resource that belongs to a collection and the target of the link is the collection to which it belongs. It is the inverse of the item relation type. In CDIF, the target name and description (not in example to left) can provide additional information about collection. |

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/tbd.md

# to be determined

---
### Source Document: metadata/technicalexpressionmetadata.md

# Technical Expression of Metadata
In the CDIF framework we think of things on the World Wide Web as Digital Objects. Metadata objects are a special kind of digital object that describe and document things on the web. To guide metadata aggregators and search engines to find metadata to index the framework recommends using existing web technology and emerging conventions. 

The Internet and World Wide Web constitute an immense body of data, information, and knowledge accessible to anyone with a computer that can interact with the system. The Web can be thought of as a library containing a large fraction of the written, recorded, and graphic works of humanity, or as a database containing an almost unimaginable spectrum of data from scientific research, historical records, government records, sensor networks, etc.

The challenge with this mountain of resources is to find particular nuggets useful to answer questions and solve problems. Addressing this problem requires, _first_, understanding what kinds of things the World Wide Web offers, referred to as '**resources**' in this discussion. _Second_, how are these resources described and documented such that they are useful? _Third_, how can descriptions of resources be made available on the Web to guide users to find and use the resources? 


## Digital Objects
A resource is an identifiable thing of interest to someone; it might be a Digital Object (DO) or a Non-digital Resource. A Digital Object is a packaged, identifiable sequence of digital bits that carries some information. A Digital Object has exactly one digital representation: a bitstream. The Digital Object bitstream might be the resource of interest, or it might be a representation of an abstract or physical resource that cannot be transmitted electronically (see [HTTP Range-14](https://en.wikipedia.org/wiki/HTTPRange-14) ). The identifier for a Digital Object can be dereferenced to access the object directly. A non-digital resource is a material entity (e.g. person, rock sample), an abstract entity (e.g. Donald Duck, The Land of Oz), or a 'Work' or 'Expression' in the [FRBR sense](https://www.loc.gov/cds/downloads/FRBR.PDF) (e.g. Beethoven's 9th Symphony, Dickens' 'Tale of Two Cities'). Identifiers for non-digital resources must dereference on the Web to a Digital Object that is a representation of the non-digital thing and can be transmitted electronically.

In the FAIR Digital Object Framework (FDOF), a Digital Object (DO) is a specific bit stream that carries some information and has a persistent, registered, resolvable identifier (PID) that can be resolved to obtain a PID kernel record. Note that 'Digital Object' is capitalised in this document to emphasise that it is being used in this specific sense. The PID kernel record provides documentation for the source of the PID, expected lifetime, type of resource it identifies, linkage to the resource it identifies, and other attributes specified in a schema identified in the PID kernel record [PID profile (Weigel et al., 2018)](https://doi.org/10.15497/RDA00031). The PID kernel record is a metadata record conforming to a particular PID profile.

Digital Objects are FAIR (FDOs) when they are part of an ecosystem comprising services and infrastructure to support realisation of the FAIR (Findable, Accessible, Interoperable, Reusable) principles. In the FAIR Digital Object Framework (FDOF) there must be a mechanism to access either the object or its metadata by dereferencing the object’s PID. Metadata content must enable the identified resource to be found, used and cited, enable interoperability and reuse, and include machine-actionable statements about dependencies and licensing. [Bonino et al. (2022)](https://fairdigitalobjectframework.org/) propose some approaches to access the FDOFIdentifierRecord (Kernel metadata) and other FDOF requirements; the level of adoption for this approach is uncertain.

## Metadata
In order for resources to be discoverable on the Web, the search applications that are used to find things must locate some representation of the resource and must be able to parse that representation and generate indexes for searching. In the realm of linked HTML Web pages, search engines parse the text content and links on Web pages to create text-based indexes and use links to find other pages to crawl the Web. This approach does not work for datasets, images, sound recordings, videos, and other non-narrative text resources, so separate representations of their content are constructed as metadata, in a format that can be parsed and indexed by search applications. This pattern is also applied to text resources to provide more explicit documentation. At the simplest level the content of the metadata can consist of text describing the resource and a link to access the resource, analogous to what is included on the cards in a legacy library card catalogue. Representing the metadata content using a structured, machine-readable format makes the information more precise and accessible to software agents.

### Metadata content
In the digital world, a wide variety of metadata schemes have evolved for describing resources. These schemes are structured to allow a richer understanding of the information, and typically at least include information about the set of fifteen generic elements identified as the Dublin Core: Creator, Contributor, Publisher, Title, Date, Language, Format, Subject, Description, Identifier, Relation, Source, Type, Coverage, and Rights, [first drafted at a 1995 meeting in Dublin, Ohio](https://www.dublincore.org/resources/metadata-basics/). These elements are defined at an abstract level and served well with free text content values for use by humans. Such semi-structured metadata is insufficient to support machine-actionable reuse of the described resources.  In order to be machine-actionable, the structure, syntax, and element-value representations in a metadata document must conform to conventions that client software can be programmed to parse and ‘understand’. ‘Understand’ in this context means recognise the incoming bitstream content and take appropriate, useful action. The metadata provider must communicate the conventions used to serialise the metadata they provide. Ideally this is done with an identifier for a specification document that details the conventions used. Some widely used metadata specifications include [DCAT](https://www.w3.org/TR/vocab-dcat-3/), [DataCite Schema](https://schema.datacite.org/), [ISO 19115-1](https://www.iso.org/standard/53798.html), [EML](https://eml.ecoinformatics.org/), [FGDC CSDGM](https://www.fgdc.gov/metadata/csdgm-standard), [CERIF](https://eurocris.org/eurocris_archive/cerifsupport.org/cerif-in-brief/index.html), [schema.org](https://schema.org/), and [DDI](https://ddialliance.org/Specification/). These specifications determine the structure and syntax of metadata documents, but leave latitude on how the values of some metadata elements are represented, and often offer multiple valid approaches to representing the same information.

### Metadata profiles
Achieving the level of metadata interoperability required for CDIF will require the adoption of one (or a small number of) metadata specification(s), along with more specific conventions on vocabularies used for metadata properties. We refer to such a set of specific conventions as a profile. CDIF provides recommendations for a metadata profile compatible with machine processing. This profile includes the base file MIME-type, an information model for the metadata content, and how that information is represented both syntactically and semantically. Most profiles are based on an existing metadata specification, e.g. schema.org, DCAT, ISO19115-1, EML, DDI-CDI, but provide additional detail to resolve ambiguities in the base specification, or rules for vocabularies and data types for element values that extend or restrict the base specification. The simplest presentation of a profile specification can be a text document that describes the information required, identifies the base specification, and states any conventions or rules for profile conformance. Such a document could be used by a software developer writing code to use information in metadata conforming to the profile. Profiles might also be specified in a machine-actionable way, e.g., the [Dublin Core Tabular Application Profiles (DCTAP)](https://www.dublincore.org/specifications/dctap/), [Profiles Vocabulary](https://www.w3.org/TR/dx-prof/), [SHACL rules](https://www.w3.org/TR/shacl/), [XML schematron rules](https://www.schematron.com/), or other schema or rule representations. Using a rule-based representation for metadata profiles provides an approach to defining and communicating metadata constraints that can be validated automatically to support metadata profile interoperability, reusability, and quality.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: metadata/validation.md

# Validation of CDIF metadata documents

One of the requirements for all CDIF conformant metadata records is the inclusion of conformance declaration that is part of the record. This is implemented in the schema.org JSON-LD implementation with a schema:subjectOf key that has @Type schema:Dataset and schema:additionalType dcat:CatalogRecord. We refer to this as the catalog record part of the metadata-- metadata about the metadata. The catalog record includes a dcterms:conformsTo statement that is a list of object references for the profiles the document conforms to. 
```
"schema:subjectOf": {
"@id": "ex:gom-water-quality-wide-2025/catalog-record",
"@type": ["schema:Dataset"],
"schema:additionalType": ["dcat:CatalogRecord"],
....
"dcterms:conformsTo": [
  {"@id": "https://w3id.org/cdif/core/1.1"},
  {"@id": "https://w3id.org/cdif/discovery/1.1"},
  {"@id": "https://w3id.org/cdif/data_description/1.1"}
]  }
```

The conformance uris are set up to resolve as follows:
- Bare uri (e.g.) "https://w3id.org/cdif/core/1.1" resolves to the implementation guide in the release repository. 
- URI with '/schema' appended resolves to the JSON schema for the profile. This schema only validates for classes and properties defined in the profile.
- URI with '/shacl' resolves to a file with SHACL rules to validate the classes and properties defined in the profile.

Thus, to validate an instance document that declares conformance to more than one profile, each profile validation artefact (schema or shacl) must be retrieved and used to test the instance. The CDIF team has implemented a python code to execute this validation workflow. In the https://github.com/Cross-Domain-Interoperability-Framework/validation github the program is ConformanceValidate.py  

To facilitate simple JSON schema validation for common instance documents that use [core + Discovery](https://github.com/Cross-Domain-Interoperability-Framework/doc-corediscovery/blob/main/CDIFDiscoveryProfileStructuredSchema.json), [core + Discovery + DataDescription](https://github.com/Cross-Domain-Interoperability-Framework/doc-discoverydatadescription/blob/main/CDIFDataDescriptionProfileStructuredSchema.json), or [core + Discovery + DataDescription + DataStructure](https://github.com/Cross-Domain-Interoperability-Framework/doc-discoverydatadescriptionstructure/blob/main/CDIFDiscoveryDataDescriptionStructureProfileStructuredSchema.json), composite schema are linked here.  

---
### Source Document: universals/univgeography.md

# Geography
In order to support discovery and selection of datasets, we need to:
1. describe the spatial extent or footprint of a dataset (e.g. name, bounding box)
2. Say something about the spatial distribution and representation of values within a dataset (e.g. grid definition, point-cloud, precision, spacing)

Where not specifically indicated in CDIF, location should be expressed according to the pattern ( value , location-system or authority [ , time ] ), for example:
- (coordinate geometry, Coordinate Reference System (, date) )
- (placename, Gazetteer (, date) )
- (cell id, grid definition)

## Location systems
There are many different location systems, including:
- Coordinate-based location, used for
	- Point location
	- Bounding box
	- Polygon
- Addresses, delivery points, lot numbers
- Named places, points-of-interest
- Named areas:
	- Administrative areas (many ranks and functions)
	- Post-codes
	- Electoral districts
	- Statistical areas
- Grids, DGGS

Different applications use different systems, reflecting information requirements which often cannot be controlled by those managing or disseminating data (e.g., in the natural sciences you may find coordinates or grid-cells, where dissemination and implementation science might use coordinates or point-of-interest, social scientists and official statisticians would use named areas, statistical areas, or administrative areas, and utilities might use addresses or post-codes).

It is often best to describe locations using the systems employed by the creator of the data, leaving it up to the data integrator to perform needed translations, because the approach to harmonising locations can be driven by the methods employed for analysis and depend on the research question in a particular case. What we can do, however, is to make sure that needed information is present to unambiguously understand the locations as described. The following sections look at some of the common location systems in use.

## Coordinate-based location

### Coordinate values

For points, lines, and polygons (including bounding-boxes) coordinate-based locations are used, usually longitude and latitude, in decimal-degrees.

- It is important to pay attention to the coordinate sign: longitudes in the western hemisphere (west of the Greenwich meridian) are negative, and latitudes south of the equator are negative.
-  Coordinate order is also important: in traditional cartographic and navigation systems the order was (latitude,longitude), i.e. (y,x); however most modern digital systems follow the more common (x,y) order from maths and graphics i.e. (longitude, latitude).

With unfamiliar data, it is always worth checking both sign and coordinate order before doing any other data manipulations.

#### Coordinate reference system
It is essential to supply a coordinate reference system (usually by reference) with any set of coordinates; without this, they are easily misinterpretated and the errors can be in kiometres on the ground.

The most commonly used coordinate reference system (CRS) for geographic coordinates is [WGS 84](https://earth-info.nga.mil/index.php?dir=wgs84&action=wgs84). This is the default system used by GPS receivers, and most Web-mapping applications, so if the CRS is not explicit it can generally be assumed to be WGS 84. This is also the default for the common geometry representations, such as [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) and the [Well Known Text Representation of Geometry (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry). However, it should be noted that WGS 84 as a satellite based system is ignorant of change in the surface of the earth (e.g. tectonic drift) so if the data relates to phenomena on or near the surface of the earth, either provide a time stamp with the coordinates or use a terrestrial reference frame, e.g. ETRS-89 (EPSG::4258) for the European tectonic plate.

The definition of a CRS involves several pieces of information, including the axis directions and measurement units, the origin location where the value is (0,0), as well as the ellipsoid that is used to approximate the shape of the earth. Some CRS are three-dimensional, including elevation. The de facto authority for definitions of coordinate reference systems is [EPSG](https://epsg.org). Properly speaking, EPSG now refers to a set of products maintained by the International Association of Oil and Gas Producers (IOGP)'s Geoinformatics Committee. These products originated with the European Petroleum Survey Group (EPSG), which merged with the IOGP in 2005. They maintain a registry with a Web API at https://apps.epsg.org/api/swagger/ui/index. The EPSG is used by many mapping software systems, and other Web copies are available (e.g. https://epsg.io). WGS 84 is denoted EPSG:4326 and the full definition can be found at https://apps.epsg.org/api/v1/CoordRefSystem/4326/export/?format=wkt.

Some jurisdictions have legal requirements to use other coordinate reference systems for some applications for official purposes. For example, the British National Grid is standard in the UK, in which the coordinates are given in metres, and the origin is fixed so that all locations within the UK have positive coordinate values. The British National Grid is denoted EPSG:27700 and the full definition is found at https://epsg.org/crs_27700/OSGB36-British-National-Grid.html or https://epsg.io/27700.

## Shapes
Point-location is defined by a single set of coordinates. Areas are usually represented by their perimeter polygon. This is defined by an ordered sequence of points, where the last point should coincide with the first in order to close the polygon. The minimum and maximum values for an extensive location define a bounding-box. The orientation of the boundaries of a bounding box align to the CRS used to describe the corners of the box. For example, for coordinates specified using latitude and longitude, the bounding box is delimited by meridians and parallels.

GeoJSON and WKT provide specific encodings. DCAT provides the following predicates that relate spatial information to a dataset:
1. dcterms:spatial for the spatial extent of the data;
2. dcat:spatialResolutionInMeters for the spatial precision or spacing of items within a
dataset.

The Global Biodiversity Information Facility (GBIF) has a geo-referencing [best practice guide](https://doi.org/10.15468/doc-gg7h-s853) that covers latitude, longitude, altitude, and depth. This is a good resource for determining good practice.

## Identifier-based location
Nominal systems associate a name or code to some spatial location or region. Commonly used cases include:
- Countries;
- Administrative units (e.g. [NUTS - Nomenclature of Territorial Units for Statistics](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics)): states, provinces, cities, local government areas);
- Statistical areas (defined by statistical agencies or census bureaus, e.g., the [Australian Statistical Geography](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026#asgs-diagram));
- Electoral districts (whose geographic footprint may change frequently so date is required);
- Postcodes.

### Reference system
In most - but not all - cases, there is a well-defined mapping of the name or code to a geospatial area. For names the list of mappings is called a gazetteer. The authority for this mapping may be well known, or may be more informal.
- Statutory naming authorities typically have a formal process for gazetting (publishing) geographic names.
- Postcodes are usually well-known and often convenient, however the exact mapping to space may be proprietary to a local postal delivery service.
- [GeoNames](https://www.geonames.org/v3/) is a crowd-sourced service that associates a point-location with many geographic names. The location used for arealy-extensive places can be inconsistent.

In many or most cases the mapping of a name to a geospatial area is time dependent. In some cases the area attached to a name is contested, for political and cultural reasons, or because of historical uncertainty. Contemporary name-based systems are generally managed nationally or locally. Historical systems are generally more difficult and there may not be an authoritative source. Geonames is a pretty good general-purpose service, but it only gives a point-location falling somewhere within the place.

## Grids
Where a dataset is composed of variables or properties whose value varies across a spatial domain, it is often represented as sampled discretely at locations on a regular grid. Discrete Global Grids (DGG) are an emerging alternative to cartesian grids.

### Reference system
The most common grid arrangement is specified in terms of an origin and axis directions (with respect to a CRS), and cell spacing. A location within the grid is then indicated by an integer index or count e.g. (234, 8916). Spatial grids may be one-, two-, three-, or four-, (spatio-temporal) dimensional.

### Usage
Spatial variation of a property across a spatial domain is commonly represented and exchanged using grids. Visualisations almost always use a cartesian (rectangular) gridded representation. Grids are the most common representation for spatial analysis and numerical modelling. Grids are convenient for data integration. However, they may need to be re-sampled or interpolated to a common orientation and spacing. Different DGGs are efficient for topology and proximity analysis, and area-based calculations.

## Addresses
Many different sources exist for the description of addresses. Among these are EPSG, ISO [19101-1:2014](https://www.iso.org/standard/59164.html) and [ISO 19107:2003](https://www.iso.org/obp/ui/#iso:std:iso:19107:ed-1:v1:en).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: universals/univintro.md

# Universals: Time, Geography, and Units of Measurement

Some information that is not domain-specific is commonly required to describe and understand resources. The use of common patterns and encodings for this information helps cross-domain interoperability. We can think of the term ‘universals’ as that metadata covering properties that are inherent in many different kinds of measurements, across many different disciplines and domains. Often, these are important in describing aspects of data which are key to the integration of data from different sources.

As a general principle, for any value in a CDIF metadata description it should be clear what value space it is taken from (i.e. scale, reference-system, or vocabulary), and this should be traceable to a suitable definition and authority. Where possible CDIF shall recommend a default approach for universals, as well as a small number of variants to accommodate commonly encountered applications.

We provide recommendations for three specific universals: space, time, and units-of-measurement (UOM). Note that practice for universals varies across disciplines according to their different requirements. For spatial data in particular, a single representation is not possible.

UOM are in some cases complex, and there is on-going discussion about how best to represent the more complex cases. In CDIF, we do not address the description of quantities at this level - we would defer to work in groups such as CODATA’s [Digital Representation of Units of Measure (DRUM) group](https://codata.org/initiatives/task-groups/drum/). This topic will be addressed more completely in future by CDIF as more clarity emerges.

## General pattern for implementation of universals
The representation of universals is always implemented in some frame of reference: (value, reference-system [, time ]). The (optional) ‘time’ value is to allow for reference-systems subject to change, where the interpretation of the value may depend on a particular version of the reference-system. In some cases, the structure of data might provide these values in an explicit way which does not require the use of patterned text (e.g., there are separate fields for each piece of the information.) When available, these should be utilised in preference to patterned text. Fields in data might contain values defined by the data schema to use a particular reference system, or each value field might be paired with a field that assigns the reference system for that value.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: universals/univtime.md

# Time
In order to support discovery and selection, we need to:
1. Describe the time period covered by a dataset (e.g., time-interval, named period, reference period)
2. Say something about the temporal representation within a dataset (e.g., precision, spacing, relative times or sequence/ordering, frequency of time series)
3. Provide information related to the time a dataset was prepared, updated, and its period of validity 

DCAT provides the following predicates that relate a time to the dataset:
1. dcterms:temporal for the temporal extent of the data.
2. dcat:temporalResolution for the temporal precision or spacing of items within a dataset.
3. dcterms:issued, dcterms:modified, dcterms:accrualPeriodicity relate to the dataset management.


The description of time will use some representation within a *temporal reference system* (TRS). The TRS must be known in order to understand the value. There are several representations of time in common use. The Open Geospatial Consortium Abstract Specification - TOPIC 25 - ABSTRACT CONCEPTUAL MODEL FOR TIME [OGC doc 23-049(draft to be published)](https://portal.ogc.org/files/?artifact_id=107087&version=2) provides a conceptual framework for these different representations. 

## Temporal coordinates
Time can be understood as involving positions along the timeline. Position can be expressed as a coordinate in a one-dimensional system. Some practical time systems use this approach explicitly:
- [Unix](https://en.wikipedia.org/wiki/Unix_time) and GPS time are based on seconds counted from an origin in 1970 and 1980, respectively.
	- GPS time is actually represented using a pair of numbers for week number plus seconds into week (optimised for low-bandwidth communication).
- Julian day counts the number of days since the beginning of 4713 BCE.
- Ordinal date counts the number of days from the beginning of a year.
- Geological applications express time in years, or millions of years [Before Present (BP)](https://en.wikipedia.org/wiki/Before_Present), which is defined as 1950 for applications where the precision of the measurement technique warrants.

Note the differing precision of these systems: seconds, days, years, millions of years. The origin of a temporal coordinate system is called the *Epoch*.

## Calendar and clock
Both calendar and clock represent a time position as a set of integer or decimal values for nested elements of progressively finer resolution: year, month, day, hours, minutes, seconds. [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) provides a textual representation or microformat which has been adopted or implemented in most encoding and software systems.

<p style="text-align: center;">Example: "2023-10-04T12:13:30.25+02:00"</p>

This should be understood as a multi-valued tuple providing values for each component of the calendar and clock. Conversion to a coordinate on a time-line can be done arithmetically except that a look-up is required to convert months to their durations in days or seconds, etc. The final two elements of the value, following '+' or '-', indicate the timezone, encoded as the hours and minutes offset from [UTC](https://en.wikipedia.org/wiki/UTC_offset). ISO 8601 uses the Gregorian calendar, whose epoch is the beginning of Year 1 CE.

While other calendars are in contemporary use within some specific communities and for some cultural applications (e.g. Traditional Chinese, Julian, Islamic, Jewish, Baha’i), the Gregorian calendar and the 24-hour clock are universally used for technical purposes.

## Ordered nominal timescales
In historical, archeological, and geological applications, dates may be expressed using a named period, tied to a recognised culture (e.g., ‘bronze age’), dynasty (e.g., ‘Tudor’), or defined by some event(s) observed in the geological record tied to the natural history of a region or the earth (e.g., ‘Proterozoic’). Some of these systems can be mapped to temporal coordinates, though calibrations may be adjusted according to new evidence156. In general, however, only the ordering relationships between members of a nominal timescale are defined - i.e. we know that a nominal date is before, after, or during some other date within the same
system, but not the size of the separation between them.

There are many nominal systems. The [International Chronostratigraphic Chart](https://stratigraphy.org/chart) and its calibration is authoritatively maintained by the [International Commission on Stratigraphy](https://stratigraphy.org/), and provides the temporal reference system used internationally in geology. Most other nominal systems are only used locally, within particular disciplinary communities.

## Recurring and periodic times
Many datasets are structured as time-series, with either regular or irregular sampling period, or frequency of observation. A sequence of time-stamps may be thought of as a one-dimensional grid.

### Usage
Time series - the periodic measurement of the same phenomenon, using the same methods, etc. - are a common way of determining trends or otherwise making observations across time. In some cases, time series are the product of data integration from disparate sources, while in other cases the data are collected as part of time series as part of their design. In the Statistical Data and Metadata Exchange (SDMX) [*Content-Oriented Guidelines*](https://sdmx.org/?page_id=3215) there is a standard enumeration of commonly used frequencies for national and supra-national official statistics. [ISO 8601-1:2019](https://www.iso.org/standard/70907.html#:~:text=This%20document%20specifies%20representations%20of,Coordinated%20Universal%20Time%20(UTC)) adds notation for recurring arbitrary intervals (e.g., 9-5, every Mon-Fri, etc.).

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


---
### Source Document: universals/univuom.md

# Units of measurement
Quantitative data is always expressed using a scale, commonly referred to as the unit of measurement (UOM). The representation of any quantity can be conceived as a ‘tuple’ comprised of:
- a number
- the scale or UOM
- (optionally) a quantity-kind, which provides context and semantics for the quantity

The quantity-kind is sometimes required because the same unit of measure can be used for incompatible quantity-kinds (e.g., energy and torque can both be quantified as Newton-metres). When encoding quantities, there are three common patterns:
- Micro-format, using a standard uom notation, and separator between the number and UOM:

<p style="text-align: center;">109.5 km/hr</p>

- Tuple or data-structure:
```
	{
	"@value" : "109.5" ,
	"@type" : "https://si-digital-framework.org/SI/units/kilometre.hour-1"
	}
```
- Fix the UOM for an array or collection, where a header or metadata gives the uom for all values, and the datastream then provides an array of values only:

<p style="text-align: center;">( "km/hr" , ( 60.4 , 75.1, 99.0, 109.5 ) )</p>

For any of these approaches the code or symbol that denotes the uom must come from a well defined system with unambiguous semantics. Note that CDIF Data Description provides properties on variables for specifying both UOM and quantity-kind (see TBD), using the micro-format described in TBD).

## UOM code systems
The following list is provided for reference, giving information about some of the common coding systems used for UOM.

**SI Digital Framework** - https://si-digital-framework.org/
- Scope: Semantic reference for SI base and derived units
- Maintained by BIPM https://www.bipm.org/en/ - the official custodian of the International System of Units (SI) https://en.wikipedia.org/wiki/International_System_of_Units
- Symbols for units follow ISO/IEC 80000 (incl special characters, superscripts etc)
  - m, eV, h, km/h
- Each UOM is denoted by a URI e.g.
  - SI Units and Quantities
    - Unit https://si-digital-framework.org/SI/units/metre
- Quantity https://si-digital-framework.org/quantities/LENG
    - Unit https://si-digital-framework.org/SI/units/pascal
- Quantity https://si-digital-framework.org/quantities/PRES
  - Non-SI units accepted for use with the SI units
    - Unit https://si-digital-framework.org/SI/units/electronvolt
- Quantity https://si-digital-framework.org/quantities/ENGY
    - Unit https://si-digital-framework.org/SI/units/hour
- Quantity https://si-digital-framework.org/quantities/TIME
  - Prefixes
    - Prefix https://si-digital-framework.org/SI/prefixes/kilo
    - Prefix https://si-digital-framework.org/SI/prefixes/nano
  - URIs for compound units based on SI Units are formulated as follows:
    - Unit https://si-digital-framework.org/SI/units/kilometre.hour-1
	
**QUDT** (Quantities, Units, Dimensions and Types) - qudt.org
- Scope: semantic descriptions of UOM for science and engineering
- Enumeration of ca. 2500 UOM - qudt.org/doc/DOC_VOCAB-UNITS.html
- Each UOM is denoted by a URI - e.g.
  - http://qudt.org/vocab/unit/M
    - http://qudt.org/vocab/quantitykind/Distance
    - http://qudt.org/vocab/quantitykind/Length
  - http://qudt.org/vocab/unit/PA
    - http://qudt.org/vocab/quantitykind/Pressure
    - http://qudt.org/vocab/quantitykind/Stress
  - http://qudt.org/vocab/unit/EV
    - http://qudt.org/vocab/quantitykind/Energy
  - http://qudt.org/vocab/unit/HR
    - http://qudt.org/vocab/quantitykind/Time
	- http://qudt.org/vocab/prefix/Kilo
  - http://qudt.org/vocab/prefix/Nano
  - http://qudt.org/vocab/unit/KiloM-PER-HR
- Local-name defined by a rule (non-opaque, almost computable)
- Dereferencing URI gets a definition of the UOM, with link to dimensionality
  - Enough information to support unit conversion
  - Codes and symbols from various systems, including UCUM, SI, and [UN/ECE Recommendation 20](https://unece.org/trade/documents/2021/06/uncefact-rec20-0)
- System also has an enumeration of ‘quantity-kinds’ - i.e. semantics
  - E.g., energy and torque have the same scale and dimensionality, but should not be transformed
- Maintained by volunteers
- Change requests processed ca. weekly - https://github.com/qudt/qudt-public-repo/issues.


**UCUM** (Unified Code for Units of Measure) - https://ucum.org/
- Scope: codes for UOM for science
- Terminal symbols plus a rule for constructing arbitrary units - extensible/scalable
- Codes match traditional scientific notation, with simplifications to match 7-bit ascii keyboard (no special characters, italics, superscripts) - e.g. km/hr, km.hr-1, N.m-2
- Maintained by [LOINC](https://loinc.org/) - Biomedical/clinical standards authority
- Change requests processed slowly - https://github.com/ucum-org/ucum/issues
- Public specification document at https://ucum.org/ucum
- Validation and conversion
  - interactive https://ucum.nlm.nih.gov/ucum-lhc/demo.html
  - API https://ucum.nlm.nih.gov/ucum-service.html.

<!-- cdif-footer-include -->
:::{include} ../_static/footer.md
:::


"""
