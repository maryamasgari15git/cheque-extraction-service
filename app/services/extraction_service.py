import asyncio
import json

import httpx

from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MODEL_TIMEOUT_SECONDS
)

from app.exceptions import ChequeAPIException
from app.prompts.cheque_prompt import CHEQUE_EXTRACTION_PROMPT
from app.models.cheque import ChequeData


client = genai.Client(
    api_key=GEMINI_API_KEY
)


MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]


async def call_gemini(
    file_content: bytes,
    mime_type: str
):

    return await asyncio.wait_for(

        asyncio.to_thread(

            client.models.generate_content,

            model=GEMINI_MODEL,

            contents=[
                types.Part.from_bytes(
                    data=file_content,
                    mime_type=mime_type
                ),
                CHEQUE_EXTRACTION_PROMPT
            ],

            config=types.GenerateContentConfig(
                temperature=0
            )
        ),

        timeout=MODEL_TIMEOUT_SECONDS
    )


def parse_model_json(text: str) -> dict:

    if not text or not text.strip():
        raise ValueError("Empty model response")

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines[0].strip().lower() in (
            "```json",
            "```"
        ):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)



async def extract_cheque(
    file_content: bytes,
    mime_type: str
) -> ChequeData:


    last_error = None


    for attempt in range(MAX_RETRIES):

        try:

            print(
                f"MODEL REQUEST ATTEMPT {attempt + 1}/{MAX_RETRIES}"
            )


            response = await call_gemini(
                file_content,
                mime_type
            )


            if not response.text:

                raise ChequeAPIException(
                    status_code=502,
                    code="MODEL_ERROR",
                    message="Empty response from model"
                )


            result = parse_model_json(
                response.text
            )


            validated_data = ChequeData.model_validate(
                result
            )


            print(
                "MODEL EXTRACTION SUCCESS"
            )


            return validated_data


        except asyncio.TimeoutError as e:

            last_error = e

            print("MODEL TIMEOUT")

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(
                    RETRY_DELAYS[attempt]
                )
                continue





        except (
            httpx.ReadError,
            httpx.ConnectError,
            httpx.RemoteProtocolError,
            httpx.TimeoutException
        ) as e:


            last_error = e


            print(
                f"MODEL CONNECTION ERROR: {type(e).__name__}"
            )


            if attempt < MAX_RETRIES - 1:

                await asyncio.sleep(
                    RETRY_DELAYS[attempt]
                )

                continue



        except json.JSONDecodeError:

            raise ChequeAPIException(
                status_code=502,
                code="INVALID_MODEL_RESPONSE",
                message="Model returned invalid JSON"
            )



        except ChequeAPIException:

            raise



        except Exception as e:

            print(
                f"MODEL ERROR: {type(e).__name__}"
            )


            raise ChequeAPIException(
                status_code=502,
                code="MODEL_ERROR",
                message=f"Model processing failed: {type(e).__name__}"
            )


    
    raise ChequeAPIException(
        status_code=504,
        code="TIMEOUT",
        message="Model response timeout"
    )


    