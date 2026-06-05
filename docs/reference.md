# 🗂️ API Reference

This section unrolls the internal codebase documentation automatically. The `mkdocstrings` plugin parses the Python source modules to extract explicit type hints, structural fields, function signatures, and Google-style docstrings in real time.

---

## ⚙️ Core Service Orchestration

The business logic layer handles internal transaction boundaries, invariants checking, and distinct validation steps before calling the persistence mechanism.

::: src.services.ContactService

---

## 📐 Domain Models Reference

These models capture the core business components and objects of the application, isolating the enterprise logic from database representations.

### 👤 Person Model
::: src.models.person.Person

### 🌐 Country Model
::: src.models.country.Country

### 📱 Number Model
::: src.models.number.Number

### 📇 Contact Aggregate Model
::: src.models.contact.Contact