# a seemingly simpler way: let the resolver find referenced documents on its own in the path
# BUT THIS DOESN'T WORK YET
# resolver = validators.RefResolver(referrer=customer_schema, base_uri=f"file:{os.path.abspath('.')}/")
# resolver.resolve('#/$defs/address') # local to the schema
# resolver.resolve('gql-defs#/gql.date') # from the referenced schema
# validator = validators.Draft202012Validator(customer_schema, resolver=resolver)
# validator.is_valid(customer_instance)
# # also try
# # result = validate(schema=customer_schema, instance=customer_instance, resolver=resolver)
# # if result == None:
# #    print("valid")