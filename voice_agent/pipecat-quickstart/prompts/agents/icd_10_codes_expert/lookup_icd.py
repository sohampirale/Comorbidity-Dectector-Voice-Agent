import csv
import asyncio
from typing import List, Dict
from langchain_core.tools import tool

@tool
async def lookup_icd(
    mandatory_keywords: list[str], additional_keywords: list[str], no_of_rows: int
) -> List[Dict[str, str]]:
    """
    Look up ICD-10 codes based on mandatory keywords.

    Args:
        mandatory_keywords: List of keywords that must be present in the results
        additional_keywords: List of additional keywords for search
        no_of_rows: Number of rows to return (maximum allowed is 30)

    Returns:
        List of dictionaries containing matching ICD-10 codes with CODE, SHORT_DESCRIPTION, and LONG_DESCRIPTION

    This function:
    - Loads entire ICD-10 CSV file
    - Searches for rows containing all mandatory keywords in SHORT_DESCRIPTION column only
    - Returns matching rows with CODE, SHORT_DESCRIPTION, and LONG_DESCRIPTION

    Examples:
        # Example 1: Patient with diabetes complications
        await lookup_icd(["diabetes"], ["mellitus", "type", "complications"], 7)

        # Example 2: Heart condition with chest pain
        await lookup_icd(["chest"], ["pain", "acute", "heart"], 5)

        # Example 3: Respiratory infection
        await lookup_icd(["pneumonia"], ["acute", "viral", "respiratory"], 6)

        # Example 4: Mental health condition
        await lookup_icd(["depression"], ["major", "recurrent", "episode"], 7)

        # Example 5: Chronic kidney disease
        await lookup_icd(["kidney"], ["chronic", "disease", "failure"], 5)

        # Example 6: Hypertension complications
        await lookup_icd(["hypertension"], ["essential", "malignant", "heart"], 6)

        Important Note: These examples serve as templates for tool usage patterns only. In practice, your keyword selection and row count must adapt dynamically to each patient's unique clinical presentation, demographic factors, and comorbidity complexity. Adjust mandatory keywords to the core condition, use additional keywords for modifiers/severity, and scale row count based on diagnostic specificity needed at runtime.
    """
    print("inside lookup_icd")

    if not mandatory_keywords:
        return []

    # Convert keywords to lowercase for case-insensitive matching
    keywords_lower = [keyword.lower() for keyword in mandatory_keywords]

    matching_rows = []

    try:
        with open("icd_10_codes.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Load entire CSV and search for matching rows
            for row in csv_reader:
                short_desc = row.get("SHORT_DESCRIPTION", "").lower()

                # Check if all mandatory keywords are present in SHORT_DESCRIPTION
                if all(keyword in short_desc for keyword in keywords_lower):
                    # Count how many additional keywords are present in this row
                    additional_count = 0
                    if additional_keywords:
                        additional_lower = [kw.lower() for kw in additional_keywords]
                        additional_count = sum(1 for kw in additional_lower if kw in short_desc)

                    matching_rows.append(
                        {
                            "CODE": row.get("CODE", ""),
                            "SHORT_DESCRIPTION": row.get("SHORT_DESCRIPTION", ""),
                            "LONG_DESCRIPTION": row.get("LONG_DESCRIPTION", ""),
                            "additional_keywords_count": additional_count,
                        }
                    )

    except FileNotFoundError:
        print("Error: icd_10_codes.csv file not found")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

    # Sort matching rows by additional_keywords_count (descending) and return top no_of_rows
    matching_rows.sort(key=lambda x: x["additional_keywords_count"], reverse=True)

    # Return only top no_of_rows results
    result = matching_rows[:no_of_rows]

    # Remove the additional_keywords_count field from final results
    for row in result:
        row.pop("additional_keywords_count", None)

    print(
        f"Found {len(matching_rows)} matching rows with all mandatory keywords in SHORT_DESCRIPTION, returning top {len(result)}"
    )
    return result


