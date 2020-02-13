# Frequency Lowering Techniques
The build of frequency lowering techniques used in hearing aid.  
This is my thesis for the degree in Computer Science.  
## Background and Aim
Hearing loss is common phenomenon that affects adults and children; it is more observed in high frequencies which are important for speech intelligibility, speech understanding in noise and localization. Common hearing aids don’t amplify properly high frequencies because of technical limits and so the contribute to high frequencies is little. Frequency lowering techniques aim to restore the audibility of high frequencies shifting them to lower frequency region where the audible capabilities of individuals are better. Every hearing aid’s manufacturer has own lowering algorithm that can be frequency compression, frequency transposition or frequency composition. These methods are commercial solution built in hearing aid and my work proposes to build one by category.
## Results
My lowering techniques are tested through combined pure tones: it is created combination of low pure tone and high pure tone. Every technique processes this tones and the expected results is a shift of the high tone to lower frequency. This is true for frequency compression and frequency transposition but not for frequency composition that generates surprisingly noise because of it is probably not suitable for pure tones.
## Conclusion
The achieved results are good but the difficult is the lack of comparison with original techniques. Moreover, the original methods works on human voice and real sounds; in the future, this work can be extended to processing real sounds.
