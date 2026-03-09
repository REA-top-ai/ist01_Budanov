tables = {
 1: ['Jiho', False],
 2: [],
 3: [],
 4: [],
 5: [],
 6: [],
 7: []}

def assign_table(table_number,name,vip_status=False):
    tables[table_number]=[name,vip_status]
    return tables

assign_table(6,'Yoni')
assign_table(4,'Карла')

print(tables)

