import pandas as pd
import re


# Alternative version using regex grep-like functionality
def grep_taxonomy_filter(taxonomy_filter, data_portal, taxonomy_file_path):
    """
    Alternative implementation using regex matching similar to grep.
    """
    
    if not taxonomy_filter or taxonomy_filter.strip() == "" or data_portal:
        return []
    
    # Column names for the taxonomy file
    column_names = ['species', 'subgenus', 'genus', 'subtribe', 'tribe', 'subfamily', 'family', 'superfamily', 'infraorder', 'suborder', 'order', 'class', 'phylum', 'kingdom', 'domain']
    
    try:
        # Read file line by line to handle inconsistent columns
        data_rows = []
        with open(taxonomy_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                parts = line.split('\t')
                
                # Ensure we have exactly 15 columns (pad with empty strings if needed)
                if len(parts) < 15:
                    parts.extend([''] * (15 - len(parts)))
                elif len(parts) > 15:
                    # If more than 15 columns, take only the first 15
                    parts = parts[:15]
                
                data_rows.append(parts)
        
        # Create DataFrame from the processed data
        df = pd.DataFrame(data_rows, columns=column_names)
        
    except FileNotFoundError:
        print(f"Error: Taxonomy file not found at {taxonomy_file_path}")
        return []
    except Exception as e:
        print(f"Error reading taxonomy file: {e}")
        return []
    
    # Create a pattern for case-insensitive matching
    pattern = re.compile(taxonomy_filter, re.IGNORECASE)
    
    # Find matches across all taxonomic columns
    hierarchy = ['species', 'subgenus', 'genus', 'subtribe', 'tribe', 'subfamily', 'family', 'superfamily', 'infraorder', 'suborder', 'order', 'class', 'phylum', 'kingdom', 'domain']
    
    matched_rows = pd.DataFrame()
    filter_level = None
    
    # Find which level contains the filter (check from lowest to highest)
    for level in hierarchy:
        mask = df[level].astype(str).str.contains(pattern, na=False)
        if mask.any():
            matched_rows = df[mask]
            filter_level = level
            break
    
    if matched_rows.empty:
        print(f"No matches found for '{taxonomy_filter}'")
        return []
    
    # Determine what to report based on hierarchical rules
    # Don't report taxonomic levels below the filter level
    if filter_level in ['species', 'subgenus', 'genus', 'subtribe', 'tribe', 'subfamily', 'family']:
        # Report families
        result = matched_rows['family'].dropna().unique().tolist()
        level_name = "Family"
    elif filter_level == 'superfamily':
        # Report families within the superfamily
        result = matched_rows['family'].dropna().unique().tolist()
        level_name = "Family"
    elif filter_level in ['infraorder', 'suborder']:
        # Report orders
        result = matched_rows['order'].dropna().unique().tolist()
        level_name = "Order"
    elif filter_level == 'order':
        # Report families within the order
        result = matched_rows['family'].dropna().unique().tolist()
        level_name = "Family"
    elif filter_level == 'class':
        # Report orders within the class
        result = matched_rows['order'].dropna().unique().tolist()
        level_name = "Order"
    elif filter_level == 'phylum':
        # Report classes within the phylum
        result = matched_rows['class'].dropna().unique().tolist()
        level_name = "Class"
    elif filter_level == 'kingdom':
        # Report phyla within the kingdom
        result = matched_rows['phylum'].dropna().unique().tolist()
        level_name = "Phylum"
    elif filter_level == 'domain':
        # Report kingdoms within the domain
        result = matched_rows['kingdom'].dropna().unique().tolist()
        level_name = "Kingdom"
    
    print(f"Found {len(result)} unique {level_name} names matching '{taxonomy_filter}' at {filter_level} level:")
    for name in sorted(result):
        print(f"  - {name}")
    
    return result
