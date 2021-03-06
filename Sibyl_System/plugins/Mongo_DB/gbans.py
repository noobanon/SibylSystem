from Sibyl_System import MONGO_CLIENT
from typing import Optional, Dict, Union
from datetime import datetime

db = MONGO_CLIENT["Sibyl"]["Main"]


async def get_gban(user: int) -> Optional[Dict[str, Union[str, int]]]:
    json = await db.find_one({"user": user})
    return json


async def update_gban(
    victim: int,
    reason: Optional[str] = None,
    proof_id: Optional[int] = None,
    enforcer: Optional[int] = None,
    message: Optional[str] = None,
) -> True:
    gbans_dict = await get_gban(victim)
    if gbans_dict:
        if reason:
            gbans_dict["reason"] = reason
        if proof_id:
            gbans_dict["proof_id"] = proof_id
        if enforcer:
            gbans_dict["enforcer"] = enforcer
        if message:
            gbans_dict["message"] = message
        gbans_dict["timestamp"] = datetime.timestamp(datetime.now())
        await db.replace_one(await get_gban(victim), gbans_dict)
    else:
        gbans_dict = {
            "user": victim,
            "reason": reason,
            "enforcer": enforcer,
            "proof_id": proof_id,
            "message": message,
            "timestamp": datetime.timestamp(datetime.now()),
        }
        await db.insert_one(gbans_dict)
    return True
