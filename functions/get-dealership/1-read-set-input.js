function main(params) {
  let result = {};
  //if param state is provided, create query to match the state, otherwise select all dealerships
  if (params.state) {
    result["query"] = {
      "selector": {
        "st": params.state
      },
      "use_index": "state_index"
    }
  }
  else {
    result["query"] = {
      "selector": {
        "id": {
          "$exists": true
        }
      }
    }
  }
  return result;
}
