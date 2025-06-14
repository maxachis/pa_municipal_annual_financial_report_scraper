


def compile_query(query):
    return query.compile(compile_kwargs={"literal_binds": True})