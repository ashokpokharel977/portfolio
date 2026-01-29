---
title: "Terraform Modules The Right Way"
description: "Building battle tested terraform modules"
pubDate: 2024-01-27
updatedDate: 2024-01-28  # Optional - only if you update the post
heroImage: "/images/blog/terraform-the-right-way/terraform-the-right-way-hero.png"  # Optional
category: "devops"  # Required - see categories below
tags: ["terraform", "automation"]  # Optional array
draft: false  # Set to true to hide from production
---
# Terraform Modules The Right Way


### Introduction

- Terraform is a powerful tool for managing infrastructure as code.
- This article outlines best practices for designing Terraform modules and automating testing for Terraform.

### Modules

- A module is a container for multiple resources that are used together.
- Key considerations while designing Terraform modules include:
    - breaking down complex modules into standalone submodules
    - including a [README.md](http://readme.md/), [CHANGELOG.md](http://changelog.md/), [versions.tf](http://versions.tf/), [variables.tf](http://variables.tf/), and outputs on each module
    - using namespaces for resources
    - locking down Terraform and provider versions.

### Automated Testing for Terraform

- Terraform testing can be broken down into several types: static analysis, unit tests, integration tests, and cleanup tests.
- Best practices for Terraform testing include:
    - using remote state with versioning and locking
    - using workspaces for multiple environments
    - never saving TF state files in git
    - including tests for each module
    - adding an examples folder to use modules
    - including in git pre-commits
    - including in CI workflows.

## What are Modules?

> A *module* is a container for multiple resources that are used together. You can use modules to create lightweight abstractions, so that you can describe your infrastructure in terms of its architecture, rather than directly in terms of physical objects.
> 

### Key Considerations while designing terraform module.

![Untitled](/images/blog/terraform-the-right-way/Untitled.png)

**Terraform Module Structure**

```bash
variables.tf: Module inputs
outputs.tf: Outputs of module and other modules that can use
README.md: Module documentation and use cases
CHANGELOG.md: Change logs and upgrade guides
examples: Use cases and examples for module usage
tests: for writing go tests with terratests
submodule: breakdown the complex module
```

```bash
$ tree complete-module/
.
├── README.md
├── main.tf
├── variables.tf
├── outputs.tf
├── ...
├── modules/
│   ├── nestedA/
│   │   ├── README.md
│   │   ├── variables.tf
│   │   ├── main.tf
│   │   ├── outputs.tf
│   ├── nestedB/
│   ├── .../
├── examples/
│   ├── exampleA/
│   │   ├── main.tf
│   ├── exampleB/
│   ├── .../
```

![Untitled](/images/blog/terraform-the-right-way/Untitled%201.png)

![Untitled](/images/blog/terraform-the-right-way/Untitled%202.png)

### Module releases

Use semantic versioning to release module.

![Untitled](/images/blog/terraform-the-right-way/Untitled%203.png)

`MAJOR`: when you make incompatible API changes

`MINOR`: when you add functionality backward compatible

`PATCH` : when you make backward-compatible bug fixes

**Module destructuring**

![Untitled](/images/blog/terraform-the-right-way/Untitled%204.png)

[Module Creation - Recommended Pattern | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation)

### Monolithic Terraform Issues

- one/several huge files
- hard to find/debug
- guess work
- slower development cycles

### Best Practices while creating a module

- Include [`README.md`](http://README.md) , [`Changelog.md`](http://Changelog.md) , [`versions.tf`](http://versions.tf) , [`variables.tf`](http://variables.tf) and `outputs` on each modules.
- Breakdown complex modules into standalone `submodules`
- Namespace all your resources.
- separate modules, tests.
- Lockdown terraform and provider versions.
- `TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache` to reuse caches
- Use `null` attribute when the field will be empty

![Untitled](/images/blog/terraform-the-right-way/Untitled%205.png)

![Untitled](/images/blog/terraform-the-right-way/Untitled%206.png)

- Include tests for each module.

![Untitled](/images/blog/terraform-the-right-way/Untitled%207.png)

![Untitled](/images/blog/terraform-the-right-way/Untitled%208.png)

- Add an examples folder to use modules.

## Automated testing for Terraform

![Untitled](/images/blog/terraform-the-right-way/Untitled%209.png)

![Untitled](/images/blog/terraform-the-right-way/Untitled%2010.png)

<aside>
🔥 What happens?
- Deploying less frequently
- Smoking and drinking

</aside>

<aside>
💡 Fight fear with confidence

</aside>

**Test types**

![Untitled](/images/blog/terraform-the-right-way/Untitled%2011.png)

- **Static analysis**
    - Compiler / parser / interpreter
        - `terraform validate`
        - VS Code:
            - [https://marketplace.visualstudio.com/items?itemName=MadsKristensen.Terraform](https://marketplace.visualstudio.com/items?itemName=MadsKristensen.Terraform)
    - Linter
        - conftest
        - terraform_validate
        - tflint
    - Dry run
        - terraform plan
        - hashicorp sentinel
        - terraform-compliance
- **Unit Tests**
There is no pure unit testing for infrastructure code.
**Terratest** `deploy and undeploy` 
Example : https://github.com/gruntwork-io/infrastructure-as-code-testing-talk
    - Deploy
    - Validate
    - Undeploy
- Other ways to validate
    - Web services: web requests
    - server: terratest ssh package
    - cloud: terratest, cli ,api
    - DB: SQL queries
- **Integration**
    - test parallelism
    - test stages
    - test retries
- **CleanUp**
    - cloud-nuke
    - aws-nuke

![Untitled](/images/blog/terraform-the-right-way/Untitled%2012.png)

**Terraform Best Practices**

– Use remote state with versioning and locking;
– Use workspace for multiple environments;
– Use for_each instead of count if it's possible;
– Never save TF state files in git, they can contain sensitive information in plain text format;
– Use modules for code reuse (DIY);

### Integrating with workflows

- Include in git precommits
    - https://github.com/antonbabenko/pre-commit-terraform
        - [`checkov`](https://github.com/bridgecrewio/checkov) required for `checkov` hook.
        - [`terraform-docs`](https://github.com/terraform-docs/terraform-docs) required for `terraform_docs` hook.
        - [`terragrunt`](https://terragrunt.gruntwork.io/docs/getting-started/install/) required for `terragrunt_validate` hook.
        - [`terrascan`](https://github.com/tenable/terrascan) required for `terrascan` hook.
        - [`TFLint`](https://github.com/terraform-linters/tflint) required for `terraform_tflint` hook.
        - [`TFSec`](https://github.com/liamg/tfsec) required for `terraform_tfsec` hook.
        - [`infracost`](https://github.com/infracost/infracost) required for `infracost_breakdown` hook.
        - [`jq`](https://github.com/stedolan/jq) required for `terraform_validate` with `-retry-once-with-cleanup` flag, and for `infracost_breakdown` hook.
        - [`tfupdate`](https://github.com/minamijoyo/tfupdate) required for `tfupdate` hook.
        - [`hcledit`](https://github.com/minamijoyo/hcledit) required for `terraform_wrapper_module_for_each` hook.
        - `env0` to run terraform and terragrunt workflows
- Include in CI workflows

### Demo

Example : https://github.com/ashokpokharel977/terraform-aws-vpc

DevOps production readiness checklist: [https://gruntwork.io/devops-checklist/](https://gruntwork.io/devops-checklist/)

### Conclusion

- Terraform is a powerful tool, but it must be used correctly to be effective.
- By following these best practices for designing Terraform modules and automating testing, you can ensure that your infrastructure will be reliable and secure.

### References

[*https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation*](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation)

[*https://www.slideshare.net/TomStraub5/developing-terraform-modules-at-scale-hashitalks-2021*](https://www.slideshare.net/TomStraub5/developing-terraform-modules-at-scale-hashitalks-2021)

[*https://www.ybrikman.com/writing/2017/10/13/reusable-composable-battle-tested-terraform-modules/*](https://www.ybrikman.com/writing/2017/10/13/reusable-composable-battle-tested-terraform-modules/)

[*https://www.slideshare.net/brikis98/how-to-test-infrastructure-code-automated-testing-for-terraform-kubernetes-docker-packer-and-more*](https://www.slideshare.net/brikis98/how-to-test-infrastructure-code-automated-testing-for-terraform-kubernetes-docker-packer-and-more)

[*https://github.com/adexltd/sparrow-sms/blob/main/.pre-commit-config.yaml*](https://github.com/adexltd/sparrow-sms/blob/main/.pre-commit-config.yaml)

[*https://www.slideshare.net/AmiMahloof/terraform-modules-restructured-217430888*](https://www.slideshare.net/AmiMahloof/terraform-modules-restructured-217430888)

[*https://www.infracost.io/*](https://www.infracost.io/)

[*https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation*](https://developer.hashicorp.com/terraform/tutorials/modules/pattern-module-creation)

[*https://nubenetes.com/*](https://nubenetes.com/)

[*https://github.com/gofireflyio/aiac*](https://github.com/gofireflyio/aiac)

[*https://github.com/gruntwork-io/infrastructure-as-code-testing-talk*](https://github.com/gruntwork-io/infrastructure-as-code-testing-talk)

[*https://developer.hashicorp.com/terraform/language/modules/develop/structure*](https://developer.hashicorp.com/terraform/language/modules/develop/structure)

[*https://gruntwork.io/devops-resources/*](https://gruntwork.io/devops-resources/)

[*https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9*](https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9)

[*https://github.com/SebastianUA/terraform-aws-glue*](https://github.com/SebastianUA/terraform-aws-glue)