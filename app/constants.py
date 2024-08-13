class Prompts:
    PARAGRAPH_PROMPT = """
    Generate a detailed and accurate paragraph description of maximum {num_chars} characters limit based on the user's input. Ensure precision and conciseness to deliver a focused and insightful description without losing any information from the input. Avoid any suggestions or misconceptions not presented in the input.
    
    Definition: A "bid for vehicle" is an offer made by a buyer to purchase a vehicle at a specific price during an auction. This involves making a monetary offer in a physical or online auction setting. Multiple buyers can place competitive bids, and the highest bid wins the vehicle. Some auctions have a reserve price, which is the minimum price set by the seller that bids must meet or exceed.
    Please follow the below guidelines:
    - Description start with only "This bid for vehicle".
    - Do not consider id, name, description, company_id, campaign_id, amount or max_amount and status keys of the vehicle.
    - Consider type and vehicle_categories keys.
    - Consider only_without_title, vehicle_titles, vehicle_uses, is_pre_1981_vehicles_supported, year_range_type, and vehicle_body_styles keys.
    - Consider only True values in the "vehicle_conditions" key. If both "only_that_run_and_drive" and "only_that_starts" are true, describe the car as being in a "Drivable Condition" without any further explanation or elaboration; Do not consider False values. If there are no True values available please don't write anything about "vehicle_conditions". If mileage is present in the vehicle conditions, It needs to be extracted.
    - Consider all makes, but if a make contains multiple models, include only one or two models. Trims and body_style within each model are not important.
    
    Note: Ensure the description is based solely on the given input. Avoid adding any additional information or suggestions not present in the input. Do not make bullet point description. Do not add the last line with any suggestions or additional information regarding the description.
    """

    IMPROVE_PROMPT = """
    Please refine the given description to make it more natural and clear, similar to the example provided below:

    Example:
    - The bid is available on a per-vehicle basis and is applicable to any vehicle category with a clean title. It is specifically designed to support pre-1981 vehicles, with a focus on cars from 1980. Eligible makes and models include AMC (such as Concord, Eagle), Cadillac (such as Deville, Eldorado), Chevrolet (such as Citation, Corvette), Dodge, Fiat (such as Brava, X-1/9), Plymouth, Saab (model 99), and Toyota. This bid is exclusive to cars and does not impose any specific conditions or mileage requirements.
    
    Note: The refined description should be based solely on the provided input, without adding any extra information, suggestions, or bullet points. Avoid including any concluding remarks or additional instructions.
    """


class ApiUrls:
    ACCESS_TOKEN = "https://staging-auth.peddle.com/identity-provider/connect/token"
    INSTANT_BID_JSON = "https://staging-service.peddle.com/buyer/v1/instant-bids/{instant_bid_id}"


class Messages:
    BLANK_PDF = "It seems that the json data you provided is blank. Unfortunately, I can't generate a description from empty content. Please upload a json with readable text."
