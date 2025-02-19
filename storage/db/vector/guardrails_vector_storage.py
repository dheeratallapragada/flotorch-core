from chunking.chunking import Chunk
from storage.db.vector.vector_storage import VectorStorage, VectorStorageSearchResponse
from guardrails.guardrails import BaseGuardRail

class GuardRailsVectorStorage(VectorStorage):

    def __init__(self, vectorStorage: VectorStorage, base_guardrail: BaseGuardRail, 
                 apply_prompt=False, apply_context=False):
        self.vectorStorage = vectorStorage
        self.base_guardrail = base_guardrail
        self.apply_prompt = apply_prompt
        self.apply_context = apply_context
    
    def search(self, chunk: Chunk, knn: int, hierarchical=False):
        if self.apply_prompt:
            guardrail_response = self.base_guardrail.apply_guardrail(chunk.data, 'INPUT')
            if guardrail_response['action'] == 'GUARDRAIL_INTERVENED':
                return VectorStorageSearchResponse(
                    status=False,
                    metadata={
                        'guardrail_output': guardrail_response['outputs'][0]['text'],
                        'guardrail_output_assessment': None, # TODO: need to add assesment
                        'block_level': 'INPUT'
                    }
                )
            
            results = self.vectorStorage.search(chunk, knn, hierarchical)

        if self.apply_context:
            result_text = ' '.join(record.text for record in results.result)
            guardrail_response = self.base_guardrail.apply_guardrail(result_text, 'INPUT')
            if guardrail_response['action'] == 'GUARDRAIL_INTERVENED':
                return VectorStorageSearchResponse(
                    status=False,
                    metadata={
                        'guardrail_output': guardrail_response['outputs'][0]['text'],
                        'guardrail_output_assessment': None, # TODO: need to add assesment
                        'block_level': 'CONTEXT'
                    }
                )
            
        return results
    
    def embed_query(self, embedding, knn, hierarical=False):
        self.vectorStorage.embed_query(embedding, knn, hierarical)

    def write(self, body):
        self.vectorStorage.write(body)

    def read(self, body):
        self.vectorStorage.read(body)