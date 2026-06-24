def run_research_pipeline(topic: str) -> dict:
    """Runs the research pipeline for a given topic."""
    state = {}  # Initialize an empty dictionary to store the research state.
    
    # Step 1: Search agent
    print("\n" + "="*50)
    print("step 1 - search agent is working ...")
    print("="*50)
    
    search_agent = build_search_agent()  # Create a search agent.
    search_result = search_agent.invoke({  # Invoke the search agent.
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content  # Store the search results.
    
    print("\n search result ", state['search_results'])  # Print the search results.
    
    # Step 2: Reader agent
    print("\n" + "="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)
    
    reader_agent = build_reader_agent()  # Create a reader agent.
    reader_result = reader_agent.invoke({  # Invoke the reader agent.
        "messages": [("user", 
            f"Based on the following search results about '{topic}', " 
            f"pick the most relevant URL and scrape it for deeper content.\n\n" 
            f"Search Results:\n{state['search_results'][:800]}")]
    })
    
    state['scraped_content'] = reader_result['messages'][-1].content  # Store the scraped content.
    
    print("\nscraped content: \n", state['scraped_content'])  # Print the scraped content.
    
    # Step 3: Writer chain
    print("\n" + "="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)
    
    research_combined = (  # Combine the search results and scraped content.
        f"SEARCH RESULTS : \n {state['search_results']} \n\n" 
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}")
    
    state["report"] = writer_chain.invoke({  # Invoke the writer chain.
        "topic": topic,
        "research": research_combined
    })
    
    print("\n Final Report\n", state['report'])  # Print the final report.
    
    # Step 4: Critic report
    print("\n" + "="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)
    
    state["feedback"] = critic_chain.invoke({  # Invoke the critic chain.
        "report": state['report']
    })
    
    print("\n critic report \n", state['feedback'])  # Print the critic report.
    
    return state  # Return the research state.