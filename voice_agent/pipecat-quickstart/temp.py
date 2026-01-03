from prompts.agents.db_expert.models import Patient
from prompts.agents.db_expert.database import get_database,init_database

async def test():
    db = get_database()
    patient = Patient()
    result = await patient.save()
    print(f'result : {result}')
    print(f'id : {result.id}')

print('db connected')
if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
