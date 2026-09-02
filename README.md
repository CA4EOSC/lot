# CLIMATE-ADAPT4EOSC

**CLIMATE-ADAPT4EOSC** (Project No: 101188248) is a Horizon Europe project dedicated to establishing a seamless, EOSC-centred collaborative research environment for climate change adaptation.

This repository specifically implements the **Legal and Organizational Interoperability (LOT)** framework for the project, providing automated tools for converting licenses into standardized, machine-readable ODRL policies.

## Project Overview

The project aims to break down existing barriers to climate data access and facilitate meaningful interactions between EOSC and various EU and national climate data spaces. By aligning with EOSC’s infrastructure plan, CLIMATE-ADAPT4EOSC ensures that data management practices are compliant with legal standards, semantically aligned for cross-disciplinary research, and technically robust.

### Core Objectives

1.  **Data FAIRification**: Deploying the `CLIMATE-ADAPTdata4EOSC` service to generate and share FAIR data, metadata, and digital research objects.
2.  **Innovative Services**: Implementing the `CLIMATE-ADAPTservice4EOSC` suite, featuring:
    *   **OPENHIDRA**: Coastal/port climate adaptation service.
    *   **3SES (Shrink-Swell from Space2Earth Service)**: Static and dynamic mapping of shrink-swell risks for infrastructure.
    *   **Just-CURS**: Urban climate resilience service for socially vulnerable communities.
    *   **BDAnalytics**: AI-guided open-source big data analytics framework.
3.  **Interoperability**: Developing five interoperability frameworks (Technical, Semantic, Cross-domain, Organisational, and Legal) to enhance data exploitation and services within the EOSC.

## Decentralized Identity (DID) Framework

This project utilizes ODRL-based decentralized identifiers (DIDs) to ensure verifiable provenance and secure attribution for all project outputs and participants. DIDs can be resolved via the [Universal Resolver](https://dev.uniresolver.io/).

### Project DID Hierarchy

The project operates under a root DID: [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz)

### Project Partners Inventory

| No. | Short name | Full name | Country | Project DID | Country DID | Partner DID | Core Contribution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | NCSRD | NATIONAL CENTER FOR SCIENTIFIC RESEARCH "DEMOKRITOS" | Greece | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmQUuKx7P2xxd2ugaeFjfujLNDSRjgBdLcPwRsRXS4gZUy) | [DID](https://dev.uniresolver.io/#did:oyd:zQmciJaGKx3WKs1GGM6SLqsK7G6vgQkBpm3HyVeHDWkRX4Z) | Project coordination (WP8), multi-scale climate hazard simulation, HPC/digital twin modeling. |
| 2 | ART | ARTELIA | France | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhUABeBZp7egwXSPJicMiJ3QPHXTejicfthPU5DcUwrm) | [DID](https://dev.uniresolver.io/#did:oyd:zQmRCQtN5rWzKcxxW8c8yQkSW7Mv9LhGzNEHKs4VKnhbHbm) | WP6 lead; engineering services for water/energy; lead on clay risk assessment/mapping (UC3). |
| 3 | LNEC | LABORATORIO NACIONAL DE ENGENHARIA CIVIL | Portugal | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmc4xvBiRBXQP64dsfrR23mtYswGoziyPH4MqhgWS2ZEeo) | [DID](https://dev.uniresolver.io/#did:oyd:zQmew1yQWZmZuG5BPgLpRyKDYsx4qCHq79bJtRomb9EuMYG) | WP5 lead (demonstrations); hydrodynamic/coastal forecasting (OPENCoastS/HIDRALERTA). |
| 4 | INCD | ASSOCIACAO INCD | Portugal | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmc4xvBiRBXQP64dsfrR23mtYswGoziyPH4MqhgWS2ZEeo) | [DID](https://dev.uniresolver.io/#did:oyd:zQmbVWBhDYqnAKYaCjnAqypZkjgN4f7uRNcPoa2t9eFT4N6) | Infrastructure provider (EOSC/EGI cloud); technical deployment and integration support. |
| 5 | TVS | TECHNOVATIVE SOLUTIONS LTD | United Kingdom | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmdoxjZe8KZv7UF9TQMtwFbTsruPjQbVmofgCTuQcHRJq5) | [DID](https://dev.uniresolver.io/#did:oyd:zQmStSc3sjhZPafBcr6VvXrUsyetChsri4aTZARvyXGXZHp) | WP1 lead; AI/ML model architectures, climate adaptation toolkits, big data analytics (BDAnalytics). |
| 6 | UCAM | THE CHANCELLOR MASTERS AND SCHOLARS OF THE UNIVERSITY OF CAMBRIDGE | United Kingdom | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmdoxjZe8KZv7UF9TQMtwFbTsruPjQbVmofgCTuQcHRJq5) | [DID](https://dev.uniresolver.io/#did:oyd:zQmeBigH9GUbKRNkkwa8nG53uGbXoCBZXtWhUMXhmvnzCve) | WP4 lead; cross-domain knowledge graphs, HPC (CSD3) analysis, semantic interoperability. |
| 7 | UNIMAN | THE UNIVERSITY OF MANCHESTER | United Kingdom | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmdoxjZe8KZv7UF9TQMtwFbTsruPjQbVmofgCTuQcHRJq5) | [DID](https://dev.uniresolver.io/#did:oyd:zQmcUipfZikytiym7QTNG1wXW9R98SQNchpFFppGHaKRMJB) | WP2 lead; provenance/FAIR expert, RO-Crate development, privacy-preserving policy engine. |
| 8 | GAC | GAC | France | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhUABeBZp7egwXSPJicMiJ3QPHXTejicfthPU5DcUwrm) | [DID](https://dev.uniresolver.io/#did:oyd:zQmUQYyEVr4cwz9BrYxiwv8CND9m9S6uQT4LwEeA5o6GTTX) | WP7 lead; policy dialogue, project dissemination, communication, and exploitation strategy. |
| 9 | CODATA | COMITE DES DONNEES SCIENTIFIQUES ETTECHNOLOGIQUES ASSOCIATION | France | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhUABeBZp7egwXSPJicMiJ3QPHXTejicfthPU5DcUwrm) | [DID](https://dev.uniresolver.io/#did:oyd:zQmaXhEhYFR5gpgkRfiGkkTDstcHuNPdwoq65JYmzQibCSJ) | WP3 lead; Data policy & legal interoperability; Cross-Domain Interoperability Framework (CDIF). |
| 10 | NOA | ETHNIKO ASTEROSKOPEIO ATHINON | Greece | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmQUuKx7P2xxd2ugaeFjfujLNDSRjgBdLcPwRsRXS4gZUy) | [DID](https://dev.uniresolver.io/#did:oyd:zQmWHsq6ypnZNU4BVaRob7oAaJ4CaEiSdUiPFAy4MmDY89R) | Weather/climate prediction; climate indicators, high-resolution micro-climatic modeling. |
| 11 | EGL | DIMOS EGALEO | Greece | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmQUuKx7P2xxd2ugaeFjfujLNDSRjgBdLcPwRsRXS4gZUy) | [DID](https://dev.uniresolver.io/#did:oyd:zQmVKT8NMpuPnD2eGWs8rw8aWcpdMJqNwi6Sb5PAdvSyvfi) | Piloting partner, user validation, urban resilience (Just-CURS) demonstration site. |
| 12 | APA | APA-ADMINISTRACAO DO PORTO DE AVEIRO SA | Portugal | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmc4xvBiRBXQP64dsfrR23mtYswGoziyPH4MqhgWS2ZEeo) | [DID](https://dev.uniresolver.io/#did:oyd:zQmfTkVfKSjH4AwjqzVa6wBpNSmNY3vCvih11XLNE5BhPfj) | Portuguese data space provider; Aveiro port management/demo infrastructure provider. |
| 13 | CSTB | CENTRE SCIENTIFIQUE ET TECHNIQUE DU BATIMENT | France | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhUABeBZp7egwXSPJicMiJ3QPHXTejicfthPU5DcUwrm) | [DID](https://dev.uniresolver.io/#did:oyd:zQmTEaatuDCSu5ZDTHz4ACRjqmNgRLAhvQ76qsNPkxFvSFv) | Building/territory resilience expert; end-user validation for UC3 (clay risk). |
| 14 | DATA4 | DATA4 SERVICES POLAND SP. Z O.O. | Poland | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmRoHFEH6DxaC9UMb6RbP1tkxMSEuYBeyHcYMPTZD1hwYq) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhczKjfCQcfNptEN5YKci55Lt6U4LsHmRaKtkX234f2A) | Data center provider; industrial operational validation for UC3 (clay risk) in Poland. |
| 15 | NVTP | NOVITOPIA BILGI TEKNOLOJILERI LIMITED SIRKET | Türkiye | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmRW7G6Gh7CxEe8vMtxnNMkoWXJh8H2CirTYaaDi321SM1) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPn1yY94jAKnvgqHbzjDymidgVCdghNqqcNiT9uCrgbBZ) | Full-stack dev; ML implementation, software development for project services (WP2, WP4, WP5). |
| 16 | BRGM | BUREAU DE RECHERCHES GEOLOGIQUES ET MINIERES | France | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPhUABeBZp7egwXSPJicMiJ3QPHXTejicfthPU5DcUwrm) | [DID](https://dev.uniresolver.io/#did:oyd:zQmaAerL9gGvgBYtau5SR7TXvnYYZryVt2dj2eqDDM8JAuh) | Geological survey expert; end-user validation for UC3 (clay risk), hydrogeological expertise. |
| 17 | SIKT | SIKT - KUNNSKAPSSEKTORENS TJENESTELEVERANDOR | Norway | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmZvZTwGjt63br3L7DTWMFb6FWAy77NdZjhg3FPvfzRMT1) | [DID](https://dev.uniresolver.io/#did:oyd:zQmPQyJ6uSvMwP77gKd971X9317EAFADaNqfZY6CbLocf2h) | Data sharing/open research services; CDIF collaboration, organizational interoperability framework. |
| 18 | IANUS | IANUS TECHNOLOGIES LTD | Cyprus | [DID](https://dev.uniresolver.io/#did:oyd:zQmR9CZUoFqBAt9TyPqMrjs3KBXBky3LPJd8UvMuPTASdvz) | [DID](https://dev.uniresolver.io/#did:oyd:zQmd2dFohbChVEhM2H1SSqjst1UoRAbcgmjpPCgXmzczrdV) | [DID](https://dev.uniresolver.io/#did:oyd:zQmWtXNW429c5jtgeU3ywsGfHD3mNherrv5NpN6hyS8RmJm) | Digital tools for risk management; urban vulnerability software, IT support, replication (Cyprus). |

## Legal and Organizational Interoperability (LOT)

As a core part of the CLIMATE-ADAPT4EOSC mission to build interoperability frameworks, this repository implements the **Legal and Organizational Interoperability (LOT)** framework. 

A central component of this framework is the automated translation of complex software and data licenses into machine-readable **ODRL (Open Digital Rights Language)** policies. 
By converting these diverse legal constraints into standardized, CDIF-compliant ODRL profiles, the LOT framework ensures that automated systems can reliably parse, understand, and enforce data rights and organizational compliance across the EOSC ecosystem.

The tools, models, and scripts used to perform this automated ODRL conversion—as well as the resulting generated JSON-LD policy files—are hosted inside the `ODRL/` directory within this submodule.
