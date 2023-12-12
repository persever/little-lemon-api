def is_valid_single_field_req(self, fieldname):
    return self.request.data.get(fieldname) and len(self.request.data) == 1