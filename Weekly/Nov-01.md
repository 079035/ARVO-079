# Instrcution
        - Current Best Success Rate: 5% (32/571)
        - False Positives
            - Insert "break", "return", and additional but not meaningless checks to avoid fuzzer crash
            - Functional Check is needed
                - Idea is very simple: We can just compile "something" of real-fixed and codex-fixed binary -- Case 4097
                - "something" could be a function call, or trace ..; which means we need a platform to analyze the binary execution
                - It's not a critical problem now, so shall we do it later 
        
        - Some cases are not supposed to be fixed, such as
            - Very complex cases which insert hundreds of lines
            - Additional information is used
                - such as a string should be less than 8 bytes 
                - or it would lead to buffer overflow later
                - So how do we know, for example, a variable (which represents the length of a string) should be less than 8 rather than 9 -- case 340
                - In my view, these cases are supposed to be not fixable by AI with limited code segments
            - Should we select 30~50 cases and find if we can provide good instructions to fix them and summarize the common features that can help Codex to create new strategies

        - We need more information, such as 
            - If it's Off-By-One (Easy to fix for Codex)
            - If it's UAF (Easy to fix for Codex)
            - If it's un-init memory (Easy to fix as long as we tell Codex which variable is not init)
            - ...
            - What we need is more information about the vulnerability
